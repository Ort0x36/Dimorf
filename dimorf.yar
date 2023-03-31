rule MAL_PY_Dimorf
{
	meta:
		author = "Silas Cutler"
		description = "Detection for Dimorf ransomware"
		date = "2023-01-03"
		version = "1.0"
		ref = "https://github.com/Ort0x36/Dimorf"

	strings:
		$func01 = "def find_and_encrypt"
		$func02 = "def check_os"
		$func03 = "def __save_log_error"
		
		$comment01 = "checks if the user has permission on the file."

		$misc01 = "/log_dimorf"
		$misc02 = ".dimorf"

	condition:
		all of them
}
