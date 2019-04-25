<?php
/**
 * 
 */
class sshconnect
{
	public $ssh_server = "192.168.1.10";
	public $ssh_port = "22";
	public $ssh_username = "";
	public $ssh_password = "";
	public $ssh_cmd = "";


	
	function connect()
	{
	$connection = ssh2_connect($this -> ssh_server , $this -> ssh_port);
	ssh2_auth_password($connection,$this -> ssh_username, $this -> ssh_password);
	$stream = ssh2_exec($connection, $this -> ssh_cmd);
	stream_set_blocking($stream, true);
	$stream_out = ssh2_fetch_stream($stream, SSH2_STREAM_STDIO);
	echo stream_get_contents($stream_out);

	}
}

$obj = new sshconnect();
$obj -> ssh_cmd = "ping 8.8.8.8 -c 4";
$obj -> connect();


?>
