
# Enhancing Malicious IP Detection and Intelligence Using Abuse.ch API

I recently finished a project aimed to improve the detection and threat intelligence of malicious IPs on an organization's network and assets.

## Summary

*The project leveraged Wazuh as the SIEM tool (Other SIEM tools include Splunk, Microsoft Sentinel, IBM QRadar), [abuse.ch](http://abuse.ch) as the indicator of compromise source, and a Python script that pulls the malicious IP address from [abuse.ch](http://abuse.ch) using an API, into the Wazuh manager.*

*The Wazuh manager executes the scripts every six hours using a cron job, and saves the output of the script to a separate file. This file gets referenced by another file containing the detection rule which all agents connected to the Wazuh server/manager are to obey.*

*The aim of the project is to enhance an organization's IP intelligence by detecting more malicious IP addresses which automatically gets fed into the detection rules, thereby blocking those IP addresses labeled as malicious from accessing our organization’s network.*

> ***The flow is as follows: Wazuh runs a Python script which pulls malicious IP addresses into a file. This file gets checked by the Wazuh manager when an IP shows up in the logs, and if there is a match, the active response kicks off.***

## Requirements

*   A Wazuh Server/Manager - This must run on a Linux machine.
*   Wazuh Agents: Windows, Linux, MacOS
*   Python 3.9 for writing and executing the Python’s script.
*   MalwareBazaar’s API

## Set Up

Refer to this [guide](https://chisom.hashnode.dev/setting-up-a-wazuh-project-a-siem-and-xdr-platform-from-scratch) to set up Wazuh.

On your Wazuh Server/Manager, install Python 3

```bash
sudo apt update -y && sudo apt upgrade -y sudo apt install python3

````

Confirm your installation using:

``` bash
python -version     
```

Create your python script. This script pulls the malicious IP address from MalwareBazaar using the abuse.ch feature API. 

[See script here](abuse.py)

Make the script executable using this command:

``` bash
chmod +x /usr/local/bin/abuse.py

```

Create a cron job to run the script every 6 hours

First, I need to enter the cron tab:

``` bash
sudo crontab -e

```

Then paste the cron command at the end of the contents:

``` cron
0 */6 * * * /usr/bin/python3 /usr/local/bin/abuse.py

```

Once you are done with this, navigate to the directory bearing the local\_rules.xml

You may want to login as root to be able to access this file as it is within the Wazuh configuration environment.

Run: `sudo -i` to login as root

Navigate to `cd /var/ossec/etc`

Navigate to the rules directory using `cd rules`, then open the `local_rules.xml` file using the `nano local_rules.xml` command
[Check here for the rules](local_rules.xml)


After setting this rule, restart the wazuh manager, then check for its status:

``` bash
systemctl restart wazuh-manager
systemctl status wazuh-manager

```

Once you confirm that your manager is active and running, check that the script runs:

``` bash
sudo /usr/bin/python3 /home/chisom/abuse.py

```

Running this command should execute the script, navigate back to your `malicious_ips_list.txt` folder, then access the file, you should see lots of IP addresses.

## Active Response

The ip addresses in the `malicious_ips_list.txt` file would be checked by Wazuh anytime a log bearing an IP address shows up from an agent, and if there is a match, an alert is triggered on the dashboard.

However, to take this further, we can decide to set up an active response for automated actions especially in situations where our agents often face brute force attacks (brute force attack logs often carry IP addresses).

For instance, if we want to drop all malicious IPs, we can configure our active response to read the `local_rules.xml`, and execute accordingly.

Since I am leveraging the `firewall-drop` script, a default Active Response script on Wazuh, I simply need to navigate to the active response directory: `cd /var/ossec/etc`

Open the `ossec.conf` file, and locate the active response section, paste your rule, something like this at the end of the section:

Access the [ossec.conf here](ossec.conf)



Restart your Wazuh manager using `systemctl restart wazuh-manager`, and `systemctl status wazuh-manager`.



Once this is done, any IP address pulled by the [abuse.py](http://abuse.py) script that shows up on any agent’s log will be dropped for 6000 seconds which is 100 minutes. You can increase the time limit as you wish.

Check [images here](images)
