Lists and sorts all Tetra Definitions by modification date.
		
	select path, datetime(mtime, 'unixepoch') as "Modified Time" FROM file WHERE path LIKE "C:\Program Files\Cisco\AMP\tetra\plugins\%%" order by mtime;

Linux - Detects anything monitoring keystrokes that is using pseudo-terminal to  possibly allowing them to  determine effective length of an password being typed in.

	select * from file where path = '/dev/ptmx0';
		
List all processes identifications and names in order by total memory size limited by 15 items.
	
	select pid, name, ROUND((total_size * '10e-7'), 2) AS memory_used FROM processes ORDER BY total_size DESC LIMIT 10;

select * from apps where bundle_identifier = 'com.ht.RCSMac' or bundle_identifier like 'com.yourcompany.%' or bundle_package_type like 'OSAX';

select * from launchd where label = 'com.ht.RCSMac' or label like 'com.yourcompany.%' or name = 'com.apple.loginStoreagent.plist' or name = 'com.apple.mdworker.plist' or name = 'com.apple.UIServerLogin.plist';

Linux - List the kernel modules on Linux systems and what they are used by.

	select name,used_by from kernel_modules;

Windows, MacOS, and Linux - Lists the user identification number, username, and directory for user.

	select uid, username, directory from users LIMIT 50;

select * FROM hardware_events;

select md5 FROM hash WHERE path = '/etc/passwd';

List system name, CPU name, CPU counts, and memory count.

	select hostname, cpu_brand, cpu_physical_cores, cpu_logical_cores, physical_memory FROM system_info;

Windows, MacOS, and Linux - Lists name of process, path of process, and process identification number.

	select name, path, pid FROM processes WHERE on_disk = '0' or on_disk = '1';

select pid, cmdline FROM docker_container_processes WHERE id = '$container_id';

Lists how many containers there are and the status of them.

	select containers, containers_running, containers_paused, containers_stopped FROM docker_info;

select uid, username, directory from users LIMIT 10;

select f.directory, f.filename, f.file_id, h.sha256 FROM file f LEFT JOIN hash h on f.path=h.path WHERE f.path LIKE "C:/";

***   select directory, filename, file_id, sha256 FROM file WHERE path LIKE "C:\Users\" and filename LIKE "chrome" f.path LIKE (SELECT v from __vars WHERE n="file_path") AND f.path NOT LIKE (SELECT v from __vars WHERE n="not_file_path");

Lists all Orbital tables for use.  Dependent on host Operating System.

	select * FROM sqlite_temp_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';

Lists the process identification number, common name, and user that launched the process.
		
	select processes.pid, processes.name, users.username FROM processes JOIN users ON processes.uid = users.uid;

MacOS and Linux - Most CPU intensive processes since boot.
		
	select pid, uid, path, name, ROUND(( (user_time + system_time) / (cpu_time.tsb - cpu_time.itsb) ) * 100, 2) AS percentage FROM processes, ( SELECT ( SUM(user) + SUM(nice) + SUM(system) + SUM(idle) * 1.0) AS tsb, SUM(COALESCE(idle, 0)) + SUM(COALESCE(iowait, 0)) AS itsb FROM cpu_time ) AS cpu_time ORDER BY user_time+system_time DESC LIMIT 5;

				
Windows CPU processes since boot.

	select pid, name, ROUND((user_time + system_time)/1e+6) AS proc_time from processes where pid <> 0 order by proc_time desc limit 10;

All browser extensions from Chrome and Edge.

	select * FROM chrome_extensions WHERE chrome_extensions.uid IN (SELECT uid FROM users);

Lists all process pids, their names, and the user that has initialized them.		
	
	select processes.pid, processes.name, users.username FROM processes JOIN users ON processes.uid = users.uid;

Lists all MacOS log entries that show any AirDrops happening on the endpoints queried.
	
	select * from unified_log where category = "AirDrop" and message like "startSending to%"
	
Logs socket connections for each process, performing network communications

	select processes.name, process_open_sockets.remote_address, process_open_sockets.remote_port from process_open_sockets LEFT JOIN processes ON process_open_sockets.pid = processes.pid WHERE process_open_sockets.remote_port != 0 AND processes.name != '';

Identify the malware executable dropped within the “Users” directory (in the last 100 seconds).

	select path, size from file where path like 'C:Users%%' and mtime > (select unix_time from time) - 100 and filename != '.';

Querying start-up items and registry changes.		
		
	select path, name, type, data from registry where path like 'HKEY_USERS%%%' and mtime > (select unix_time from time) - 100;

Lists all powershell events that has occurred.  

	select time, script_text from powershell_events;

Lists files written to disk within the last 100 seconds.

	select processes.pid, users.username, processes.path from processes LEFT JOIN users ON processes.uid = users.uid WHERE processes.path != '';

Lists scheduled tasks.
		
	select name, action, path, enabled, next_run_time from scheduled_tasks;

Lists installed services.		
		
	select name, display_name, start_type, path, user_account from services;

List new certificates within the system		
	
	select common_name, issuer, strftime('%d/%m/%y',datetime(not_valid_after,'unixepoch')) as expiration_date from certificates where path = 'CurrentUserTrusted Root Certification Authorities' ORDER BY common_name;
