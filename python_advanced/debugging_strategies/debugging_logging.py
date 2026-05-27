#!/usr/bin/env python3
"""
Lab: Debugging with logging.
Goal: summarize sensor records and compute average over valid entries.
"""
import logging


def configure_logging(level=logging.INFO):
    """Configure basic logging for this script."""
    logging.basicConfig(level=level, format="%(levelname)s:%(message)s")


def is_valid_record(record):
    """Return True when record has non-empty id and numeric value."""
    return bool(record.get("sensor_id")) and isinstance(record.get("value"), (int, float))


def compute_average_valid(records):
    """Return average value considering only valid records."""
    valid_value_sum = 0.0
    valid_count = 0
    for record in records:
        sensor_id = record.get("sensor_id")
        value = record.get("value")
        logging.debug("processing record sensor_id=%r value=%r", sensor_id, value)
        if is_valid_record(record):
            valid_value_sum += value
            valid_count += 1
            logging.info("accepted sensor_id=%s value=%s", sensor_id, value)
        else:
            logging.warning("ignored invalid record sensor_id=%r value=%r", sensor_id, value)
    if valid_count == 0:
        return 0.0
    avg = round(valid_value_sum / valid_count, 2)
    logging.info(
        "final valid_value_sum=%s valid_count=%s average=%s",
        valid_value_sum,
        valid_count,
        avg,
    )
    return avg


def main():
    """Main function."""
    configure_logging(logging.INFO)
    records = [
        {"sensor_id": "A-1", "value": 10.0},
        {"sensor_id": "A-2", "value": 20.0},
        {"sensor_id": "", "value": 50.0},
        {"sensor_id": "A-3", "value": 30.0},
    ]
    average = compute_average_valid(records)
    print("Average valid value:", average)


if __name__ == "__main__":
    main()
