from pathlib import Path


REQUIRED_FIELDS = [
	"HOSTNAME",
	"ANTIVIRUS",
	"FIREWALL",
	"PATCH_STATUS",
	"FAILED_LOGINS",
	"LAST_BACKUP_DAYS",
]

NUMERIC_FIELDS = ["FAILED_LOGINS", "LAST_BACKUP_DAYS"]


def find_report_files(reports_directory):
	"""Return the text report files in the reports directory."""
	reports_path = Path(reports_directory)

	if not reports_path.is_dir():
		return []

	return sorted(
		path
		for path in reports_path.iterdir()
		if path.is_file() and path.suffix.lower() == ".txt"
	)


def read_report_file(file_path):
	"""Read a report and return its text, or None if it cannot be read."""
	try:
		return Path(file_path).read_text(encoding="utf-8")
	except (OSError, UnicodeError) as error:
		print(f"Could not read {file_path}: {error}")
		return None


def parse_report(report_text):
	"""Convert KEY: VALUE lines into a dictionary."""
	report_data = {}

	for line in report_text.splitlines():
		if ":" not in line:
			continue

		key, value = line.split(":", 1)
		key = key.strip()
		value = value.strip()

		if key:
			report_data[key] = value

	return report_data


def validate_required_fields(report_data):
	"""Return a list of missing, empty, or invalid field messages."""
	errors = []

	for field in REQUIRED_FIELDS:
		if field not in report_data:
			errors.append(f"Missing required field: {field}")
		elif not str(report_data[field]).strip():
			errors.append(f"Empty required field: {field}")

	for field in NUMERIC_FIELDS:
		if field in report_data and str(report_data[field]).strip():
			try:
				int(report_data[field])
			except (TypeError, ValueError):
				errors.append(f"{field} must be an integer")

	return errors


def convert_numeric_fields(report_data):
	"""Return a copy with valid numeric fields converted to integers."""
	converted_data = report_data.copy()

	for field in NUMERIC_FIELDS:
		if field not in converted_data:
			continue

		try:
			converted_data[field] = int(converted_data[field])
		except (TypeError, ValueError):
			pass

	return converted_data
