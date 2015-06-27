"""
p = subprocess.Popen(['expect', 'scp.expect', machine_ip, '/tmp/', machine_ip])
        p.communicate()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        paramiko.util.log_to_file("filename.log")
        ssh.connect(machine_ip, username='root', password='egnyteesc')
        stdin, stdout, stderr = ssh.exec_command('ls /usr/java/')
        data = stdout.readlines()
        for item in data:
            if 'jdk' in item:
                java = '/usr/java/' + item
                print(java)
                stdin, stdout, stderr = ssh.exec_command('cd /tmp/sc-cert; /tmp/sc-cert/install_root.sh ' + java)
                print(stdout.readlines())
                ssh.close()

"""
"""
#!/usr/bin/expect

#Usage rootssh.expect <ip>
set timeout 60
set ip [lindex $argv 0]

spawn ssh root@$ip

expect "yes/no" {
    send "yes\r"
    expect "*?assword: " { send "egnyteesc\r" }
    } "*?assword: " { send "egnyteesc\r" }

expect "# " { send "scp root@172.26.64.5:/tmp/timesync.sh /tmp/\r" }
expect "yes/no" {
    send "yes\r"
    expect "*?assword: " { send "egnyteesc\r" }
    } "*?assword: " { send "egnyteesc\r" }

expect "# " { send "sh /tmp/timesync.sh\r" }
expect "# " { send "exit\r" }

spawn ssh root@172.26.64.5

expect "yes/no" {
    send "yes\r"
    expect "*?assword: " { send "egnyteesc\r" }
    } "*?assword: " { send "egnyteesc\r" }

expect "# " { send "sh /tmp/timesync.sh\r" }
expect "# " { send "exit\r" }

interact
"""


"""
desired_cap = {'os': 'Windows', 'os_version': '8', 'browser': 'Firefox', 'browser_version': '35', 'resolution': '1920x1080' }
input_cap = {}

driver = webdriver.Remote(
    command_executor='http://<your_username>:<your_key>@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

driver.get("https://stack251.qa-egnyte.com/corp/registration/register_trial_2.html?plan=business")
if not "Egnyte" in driver.title:
    raise Exception("Unable to load google page!")
driver.find_element_by_name("txtFirstName").send_keys("Ilya")

"""