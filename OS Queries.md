Lists and sorts all Tetra Definitions by modification date.
		
		SELECT path, datetime(mtime, 'unixepoch') as "Modified Time" FROM file WHERE path LIKE "C:\Program Files\Cisco\AMP\tetra\plugins\%%" order by mtime;

Linux - Detects anything monitoring keystrokes that is using pseudo-terminal to  possibly allowing them to  determine effective length of an password being typed in.

		SELECT * from file where path = '/dev/ptmx0';
		
List all processes identifications and names in order by total memory size limited by 15 items.
		
		SELECT pid, name, ROUND((total_size * '10e-7'), 2) AS memory_used FROM processes ORDER BY total_size DESC LIMIT 10;

select * from apps where bundle_identifier = 'com.ht.RCSMac' or bundle_identifier like 'com.yourcompany.%' or bundle_package_type like 'OSAX';

select * from launchd where label = 'com.ht.RCSMac' or label like 'com.yourcompany.%' or name = 'com.apple.loginStoreagent.plist' or name = 'com.apple.mdworker.plist' or name = 'com.apple.UIServerLogin.plist';

Linux - List the kernel modules on Linux systems and what they are used by.

		select name,used_by from kernel_modules;

Windows, MacOS, and Linux - Lists the user identification number, username, and directory for user.

		select uid, username, directory from users LIMIT 50;

SELECT * FROM hardware_events;

SELECT md5 FROM hash WHERE path = '/etc/passwd';

List system name, CPU name, CPU counts, and memory count.

		SELECT hostname, cpu_brand, cpu_physical_cores, cpu_logical_cores, physical_memory FROM system_info;


SELECT name, path, pid FROM processes WHERE on_disk = '0' or on_disk = '1';

		Windows, MacOS, and Linux - Lists name of process, path of process, and process identification number.

SELECT pid, cmdline FROM docker_container_processes WHERE id = '$container_id';

SELECT containers, containers_running, containers_paused, containers_stopped FROM docker_info;

		Lists how many containers there are and the status of them.

SELECT uid, username, directory from users LIMIT 10;

SELECT f.directory, f.filename, f.file_id, h.sha256 FROM file f LEFT JOIN hash h on f.path=h.path WHERE f.path LIKE "C:/";

***   SELECT directory, filename, file_id, sha256 FROM file WHERE path LIKE "C:\Users\" and filename LIKE "chrome" f.path LIKE (SELECT v from __vars WHERE n="file_path") AND f.path NOT LIKE (SELECT v from __vars WHERE n="not_file_path");

SELECT * FROM sqlite_temp_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';

		Lists all Orbital tables for use.  Dependent on host Operating System.

SELECT processes.pid, processes.name, users.username FROM processes JOIN users ON processes.uid = users.uid;

		Lists the process identification number, common name, and user that launched the process.
		
SELECT pid, uid, path, name, ROUND(( (user_time + system_time) / (cpu_time.tsb - cpu_time.itsb) ) * 100, 2) AS percentage FROM processes, ( SELECT ( SUM(user) + SUM(nice) + SUM(system) + SUM(idle) * 1.0) AS tsb, SUM(COALESCE(idle, 0)) + SUM(COALESCE(iowait, 0)) AS itsb FROM cpu_time ) AS cpu_time ORDER BY user_time+system_time DESC LIMIT 5;

		MacOS and Linux - Most CPU intensive processes since boot
		
select pid, name, ROUND((user_time + system_time)/1e+6) AS proc_time from processes where pid <> 0 order by proc_time desc limit 10;

		Windows CPU processes since boot.
		
SELECT * FROM chrome_extensions WHERE chrome_extensions.uid IN (SELECT uid FROM users);

		All browser extensions from Chrome and Edge.
		
SELECT processes.pid, processes.name, users.username FROM processes JOIN users ON processes.uid = users.uid;

		Lists all process pids, their names, and the user that has initialized them.
		
select * from unified_log where category = "AirDrop" and message like "startSending to%"

		Lists all MacOS log entries that show any AirDrops happening on the endpoints queried.
		
select processes.name, process_open_sockets.remote_address, process_open_sockets.remote_port from process_open_sockets LEFT JOIN processes ON process_open_sockets.pid = processes.pid WHERE process_open_sockets.remote_port != 0 AND processes.name != '';

		Logs socket connections for each process, performing network communications
		
select path, size from file where path like 'C:Users%%' and mtime > (select unix_time from time) - 100 and filename != '.';

		Identify the malware executable dropped within the “Users” directory (in the last 100 seconds)
		
select path, name, type, data from registry where path like 'HKEY_USERS%%%' and mtime > (select unix_time from time) - 100;

		Querying start-up items and registry changes

select time, script_text from powershell_events;

		Lists all powershell events that has occurred.  
		
select processes.pid, users.username, processes.path from processes LEFT JOIN users ON processes.uid = users.uid WHERE processes.path != '';

		Lists files written to disk within the last 100 seconds
		
select name, action, path, enabled, next_run_time from scheduled_tasks;

		Lists scheduled tasks.
		
select name, display_name, start_type, path, user_account from services;

		Lists installed services.
		
select common_name, issuer, strftime('%d/%m/%y',datetime(not_valid_after,'unixepoch')) as expiration_date from certificates where path = 'CurrentUserTrusted Root Certification Authorities' ORDER BY common_name;

		List new certificates within the system
