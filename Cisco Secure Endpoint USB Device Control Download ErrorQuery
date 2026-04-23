SELECT y.path,y.matches,y.count FROM yara y LEFT JOIN hash h
  ON h.path = y.path
WHERE y.path = 'C:\\Program Files\\Cisco\\AMP\\local.xml'
  AND y.sigrule = 'rule amp_localxml_download_or_load_enabled { strings: $download = "<download>1</download>" $load = "<load>1</load>" condition: any of them }'
  AND y.count != 0;
