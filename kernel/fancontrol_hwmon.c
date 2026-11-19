// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Custom PC Fan Controller - Linux hwmon Kernel Driver
 * Supports 4-channel PWM control and RPM telemetry via USB
 */

#include <linux/module.h>
#include <linux/init.h>
#include <linux/usb.h>
#include <linux/hwmon.h>
#include <linux/hwmon-sysfs.h>
#include <linux/slab.h>

#define DRIVER_NAME "custom_fan_hwmon"

/* Objective Development shared open-source USB IDs */
#define USB_FAN_VENDOR_ID   0x16c0
#define USB_FAN_PRODUCT_ID  0x05dc

/* V-USB Custom Vendor Requests */
#define USB_FAN_REQ_GET_STATUS  0x01
#define USB_FAN_REQ_SET_PWM     0x02
#define USB_FAN_REQ_SET_ALL     0x03

struct fan_status_pkt {
    uint8_t  pwm[4];
    uint16_t rpm[4];
} __packed;

struct custom_fan_data {
    struct usb_device *udev;
    struct device *hwmon_dev;
    struct mutex lock;
    struct fan_status_pkt status;
    unsigned long last_updated;
};

static int custom_fan_update_status(struct custom_fan_data *data)
{
    int ret = 0;

    mutex_lock(&data->lock);
    // Refresh status if older than 500ms
    if (time_after(jiffies, data->last_updated + msecs_to_jiffies(500))) {
        ret = usb_control_msg(
            data->udev,
            usb_rcvctrlpipe(data->udev, 0),
            USB_FAN_REQ_GET_STATUS,
            USB_TYPE_VENDOR | USB_RECIP_DEVICE | USB_DIR_IN,
            0, 0,
            &data->status, sizeof(data->status),
            1000
        );

        if (ret >= 0) {
            data->last_updated = jiffies;
            ret = 0;
        }
    }
    mutex_unlock(&data->lock);
    return ret;
}

static ssize_t fan_input_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct custom_fan_data *data = dev_get_drvdata(dev);
    int index = to_sensor_dev_attr(attr)->index;
    int err = custom_fan_update_status(data);

    if (err < 0)
        return err;

    return sprintf(buf, "%u\n", le16_to_cpu(data->status.rpm[index]));
}

static ssize_t pwm_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct custom_fan_data *data = dev_get_drvdata(dev);
    int index = to_sensor_dev_attr(attr)->index;
    int err = custom_fan_update_status(data);

    if (err < 0)
        return err;

    return sprintf(buf, "%u\n", data->status.pwm[index]);
}

static ssize_t pwm_store(struct device *dev, struct device_attribute *attr, const char *buf, size_t count)
{
    struct custom_fan_data *data = dev_get_drvdata(dev);
    int index = to_sensor_dev_attr(attr)->index;
    unsigned long val;
    int err;

    err = kstrtoul(buf, 10, &val);
    if (err)
        return err;

    if (val > 255)
        val = 255;

    mutex_lock(&data->lock);
    err = usb_control_msg(
        data->udev,
        usb_sndctrlpipe(data->udev, 0),
        USB_FAN_REQ_SET_PWM,
        USB_TYPE_VENDOR | USB_RECIP_DEVICE | USB_DIR_OUT,
        (uint16_t)val,        // wValue: PWM duty
        (uint16_t)(index + 1),// wIndex: Channel (1-4)
        NULL, 0,
        1000
    );

    if (err >= 0) {
        data->status.pwm[index] = (uint8_t)val;
        err = count;
    }
    mutex_unlock(&data->lock);

    return err;
}

/* Attributes for 4 fans */
static SENSOR_DEVICE_ATTR_RO(fan1_input, fan_input, 0);
static SENSOR_DEVICE_ATTR_RO(fan2_input, fan_input, 1);
static SENSOR_DEVICE_ATTR_RO(fan3_input, fan_input, 2);
static SENSOR_DEVICE_ATTR_RO(fan4_input, fan_input, 3);

static SENSOR_DEVICE_ATTR_RW(pwm1, pwm, 0);
static SENSOR_DEVICE_ATTR_RW(pwm2, pwm, 1);
static SENSOR_DEVICE_ATTR_RW(pwm3, pwm, 2);
static SENSOR_DEVICE_ATTR_RW(pwm4, pwm, 3);

static struct attribute *custom_fan_attrs[] = {
    &sensor_dev_attr_fan1_input.dev_attr.attr,
    &sensor_dev_attr_fan2_input.dev_attr.attr,
    &sensor_dev_attr_fan3_input.dev_attr.attr,
    &sensor_dev_attr_fan4_input.dev_attr.attr,
    &sensor_dev_attr_pwm1.dev_attr.attr,
    &sensor_dev_attr_pwm2.dev_attr.attr,
    &sensor_dev_attr_pwm3.dev_attr.attr,
    &sensor_dev_attr_pwm4.dev_attr.attr,
    NULL
};

ATTRIBUTE_GROUPS(custom_fan);

static const struct usb_device_id custom_fan_table[] = {
    { USB_DEVICE(USB_FAN_VENDOR_ID, USB_FAN_PRODUCT_ID) },
    { }
};
MODULE_DEVICE_TABLE(usb, custom_fan_table);

static int custom_fan_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
    struct usb_device *udev = interface_to_usbdev(interface);
    struct custom_fan_data *data;

    data = devm_kzalloc(&interface->dev, sizeof(*data), GFP_KERNEL);
    if (!data)
        return -ENOMEM;

    data->udev = udev;
    mutex_init(&data->lock);
    usb_set_intfdata(interface, data);

    data->hwmon_dev = devm_hwmon_device_register_with_groups(
        &interface->dev,
        "custom_fan",
        data,
        custom_fan_groups
    );

    if (IS_ERR(data->hwmon_dev)) {
        dev_err(&interface->dev, "Failed to register hwmon device\n");
        return PTR_ERR(data->hwmon_dev);
    }

    dev_info(&interface->dev, "Custom PC Fan Controller attached to hwmon subsystem\n");
    return 0;
}

static void custom_fan_disconnect(struct usb_interface *interface)
{
    struct custom_fan_data *data = usb_get_intfdata(interface);
    dev_info(&interface->dev, "Custom PC Fan Controller disconnected\n");
    usb_set_intfdata(interface, NULL);
}

static struct usb_driver custom_fan_driver = {
    .name       = DRIVER_NAME,
    .id_table   = custom_fan_table,
    .probe      = custom_fan_probe,
    .disconnect = custom_fan_disconnect,
};

module_usb_driver(custom_fan_driver);

MODULE_AUTHOR("FredLab");
MODULE_DESCRIPTION("Custom PC Fan Controller USB hwmon Linux Driver");
MODULE_LICENSE("GPL");
