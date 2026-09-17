from pathlib import Path

import reports_tools


def check_security_rules(report_data):
	"""Return the security rules that need attention."""
	attention_reasons = []

	if report_data["ANTIVIRUS"] != "Enabled":
		attention_reasons.append("ANTIVIRUS is not Enabled")

	if report_data["FIREWALL"] != "Enabled":
		attention_reasons.append("FIREWALL is not Enabled")

	if report_data["PATCH_STATUS"] != "Current":
		attention_reasons.append("PATCH_STATUS is not Current")

	if report_data["FAILED_LOGINS"] >= 5:
		attention_reasons.append("FAILED_LOGINS is 5 or more")

	if report_data["LAST_BACKUP_DAYS"] > 7:
		attention_reasons.append("LAST_BACKUP_DAYS is greater than 7")

	return attention_reasons


def process_report(report_path):
	"""Read, parse, validate, and classify one report."""
	report_text = reports_tools.read_report_file(report_path)

	if report_text is None:
		return "DATA ERROR", ["The report could not be read"]

	report_data = reports_tools.parse_report(report_text)
	data_errors = reports_tools.validate_required_fields(report_data)

	if data_errors:
		return "DATA ERROR", data_errors

	report_data = reports_tools.convert_numeric_fields(report_data)
	attention_reasons = check_security_rules(report_data)

	if attention_reasons:
		return "ATTENTION", attention_reasons

	return "OK", []


def display_report_result(report_path, status, reasons):
	"""Display the status and details for one report."""
	print(f"{report_path.name}: {status}")

	for reason in reasons:
		print(f"  - {reason}")


def main():
	reports_directory = Path(__file__).resolve().parent / "security_reports"

	if not reports_directory.exists() or not reports_directory.is_dir():
		print(f"Report directory does not exist: {reports_directory}")
		return

	report_files = reports_tools.find_report_files(reports_directory)
	summary = {"OK": 0, "ATTENTION": 0, "DATA ERROR": 0}

	for report_path in report_files:
		status, reasons = process_report(report_path)
		display_report_result(report_path, status, reasons)
		summary[status] += 1

	print("\nSummary")
	print(f"Reports Processed: {len(report_files)}")
	print(f"OK: {summary['OK']}")
	print(f"Attention: {summary['ATTENTION']}")
	print(f"Data Errors: {summary['DATA ERROR']}")


if __name__ == "__main__":
	main()
