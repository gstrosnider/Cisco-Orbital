#Retrieves all Windows logon, authentication, session, lock/unlock, and logoff events:

SELECT DATETIME(TimeWritten, 'unixepoch', 'UTC') AS TimeWrittenUTC, Logfile, SourceName, EventIdentifier, Type, Message FROM Win32_NtLogEvent WHERE Logfile = 'Security' AND EventIdentifier IN (
    '4624',  -- Successful logon
    '4625',  -- Failed logon
    '4634',  -- Session logged off
    '4647',  -- User-initiated logoff
    '4648',  -- Logon using explicit credentials
    '4672',  -- Administrator privileges assigned
    '4768',  -- Kerberos TGT requested
    '4769',  -- Kerberos service ticket requested
    '4770',  -- Kerberos service ticket renewed
    '4771',  -- Kerberos pre-authentication failed
    '4776',  -- NTLM credential validation
    '4777',  -- Domain controller failed credential validation
    '4778',  -- Session reconnected
    '4779',  -- Session disconnected
    '4800',  -- Workstation locked
    '4801'   -- Workstation unlocked
  )
ORDER BY TimeWritten DESC;


### Example Outputs:

2026-08-16 01:34:30

Security

Microsoft-Windows-Security-Auditing

4672

Audit Success


Special privileges assigned to new logon.

Subject:
	Security ID:		S-1-5-18
	Account Name:		SYSTEM
	Account Domain:		NT AUTHORITY
	Logon ID:		0x3E7

Privileges:		SeAssignPrimaryTokenPrivilege
			SeTcbPrivilege
			SeSecurityPrivilege
			SeTakeOwnershipPrivilege
			SeLoadDriverPrivilege
			SeBackupPrivilege
			SeRestorePrivilege
			SeDebugPrivilege
			SeAuditPrivilege
			SeSystemEnvironmentPrivilege
			SeImpersonatePrivilege
			SeDelegateSessionUserImpersonatePrivilege



2026-08-20 00:40:13

Security

Microsoft-Windows-Security-Auditing

4647

Audit Success

User initiated logoff:

Subject:
	Security ID:		S-1-5-21-814937178-2599029845-2066795240-1001
	Account Name:		Jimmy Oslen
	Account Domain:		DESKTOP-111111
	Logon ID:		0x13396D

This event is generated when a logoff is initiated. No further user-initiated activity can occur. This event can be interpreted as a logoff event.

