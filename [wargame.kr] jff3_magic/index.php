<?php
	include "./lib/lib.php";
	if(!isset($_POST['id']))
		$_POST['id']=NULL;
	if(!isset($_POST['pw']))
		$_POST['pw']=NULL;
	if(!isset($_GET['no']))
		$_GET['no']=NULL;
?>
<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Magic</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<script>
			alert("under construction......\n....?\n(hint : swp)  :D"); // This is Hint!!
		</script>
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.jpg" alt="" /></span>
							<h1 id="title">Guest</h1>
							<p>Challenger</p>
						</div>

					<!-- Nav -->
						<nav id="nav">

								   

							<!--
								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul><li><a href="index.php" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">MemberList</span></a></li>
								<li><a href="?no=2" id="top-link" class="skel-layers-ignoreHref"><span class="">Cd80</span></a></li>
								<li><a href="?no=3" id="portfolio-link" class="skel-layers-ignoreHref"><span class="">Orang</span></a></li>
								<li><a href="?no=1" id="about-link" class="skel-layers-ignoreHref"><span class="">Comma</span></a></li>
							</ul>
						</nav>

				</div>

				<div class="bottom">

					<!-- Social Icons -->
						<!--
						<ul class="icons">
							<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
							<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
							<li><a href="#" class="icon fa-github"><span class="label">Github</span></a></li>
							<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
							<li><a href="#" class="icon fa-envelope"><span class="label">Email</span></a></li>
						</ul>
						-->
				</div>

			</div>

		<!-- Main -->
			<div id="main">

				<!-- Intro -->
					<!--
					<section id="top" class="one dark cover">
						<div class="container">

							<header>
								<h2 class="alt">Hi! I'm <strong>C0mma</strong>, I'll introduce<a href="http://html5up.net/license">&nbsp;LeaveRet</a> member<br />
								<!--site template designed by <a href="http://html5up.net">HTML5 UP</a>.</h2>
								<h2 class="alt">Who is the most handsome man?</h2>
								<p>Ligula scelerisque justo sem accumsan diam quis<br />
								vitae natoque dictum sollicitudin elementum.</p>
							</header>

							<footer>
								<a href="#portfolio" class="button scrolly">Vote</a>
							</footer>

						</div>
					</section>
					-->
				<!-- Portfolio -->
					<section id="vote" class="two">
						<div class="container">
							<header>
								<h2>Magic</h2>
							</header>
							<?php
								/******************************************
								Admin check & No Parameter Filtering..
								******************************************/
								$test = custom_firewall($_GET['no']);
								if ($test != 0){
									exit("No Hack - ".$test);
								}

								$q = mysqli_query($connect, "select * from member where no=".$_GET['no']);
								$result = @mysqli_fetch_array($q);
	
								echo $result['id']."<br>";

								if(isset($_POST['id'])){
									sleep(2); // DO NOT BRUTEFORCE
									$id = mysqli_real_escape_string($connect, $_POST['id']);
									$q = mysqli_query($connect, "SELECT * FROM `member` where id='{$id}'");
									$userinfo = @mysqli_fetch_array($q);	
								}
							?>
							<br>
							<form name="vote" method="post" action="">
								<input type="text" name="id" placeholder="ID"/><br>
								<input type="password" name="pw" placeholder="PW"/><br>
								<button type="submit" value="Vote">Submit</button>
							</form>
							<?php
								if(isset($_POST['id'])){
									if (hash('haval128,5',$_POST['pw'],false) == mysqli_real_escape_string($connect, $userinfo['pw'])) {
										echo 'Success! Hello '.$id."<br />";
										if ($id == "admin")
											echo 'Flag : '.$FLAG;
									}
									else {
										echo hash('haval128,5',$_POST['pw'], false);
										echo 'Incorrect Password';
									}
								}
							?>
							<!--
							<p>Vitae natoque dictum etiam semper magnis enim feugiat convallis convallis
							egestas rhoncus ridiculus in quis risus amet curabitur tempor orci penatibus.
							Tellus erat mauris ipsum fermentum etiam vivamus eget. Nunc nibh morbi quis
							fusce hendrerit lacus ridiculus.</p>
							-->
							<!--
							<div class="row">
								<div class="4u 12u$(mobile)">
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic02.jpg" alt="" /></a>
										<header>
											<h3>Ipsum Feugiat</h3>
										</header>
									</article>
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic03.jpg" alt="" /></a>
										<header>
											<h3>Rhoncus Semper</h3>
										</header>
									</article>
								</div>
								<div class="4u 12u$(mobile)">
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic04.jpg" alt="" /></a>
										<header>
											<h3>Magna Nullam</h3>
										</header>
									</article>
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic05.jpg" alt="" /></a>
										<header>
											<h3>Natoque Vitae</h3>
										</header>
									</article>
								</div>
								<div class="4u$ 12u$(mobile)">
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic06.jpg" alt="" /></a>
										<header>
											<h3>Dolor Penatibus</h3>
										</header>
									</article>
									<article class="item">
										<a href="#" class="image fit"><img src="images/pic07.jpg" alt="" /></a>
										<header>
											<h3>Orci Convallis</h3>
										</header>
									</article>
								</div>
							</div>
							-->
						</div>
					</section>
					
					<!--
					<section id="result" class="three">

						<div class="container">

							<header>
								<h2>Result</h2>
							</header>
					
							parturient nulla quam placerat viverra mauris non cum elit tempus ullamcorper
							dolor. Libero rutrum ut lacinia donec curae mus vel quisque sociis nec
							ornare iaculis.</p>
							
						</div>
					</section>
					-->
				<!-- Contact -->
					<!--
					<section id="contact" class="four">
						<div class="container">

							<header>
								<h2>Contact</h2>
							</header>

							<p>Elementum sem parturient nulla quam placerat viverra
							mauris non cum elit tempus ullamcorper dolor. Libero rutrum ut lacinia
							donec curae mus. Eleifend id porttitor ac ultricies lobortis sem nunc
							orci ridiculus faucibus a consectetur. Porttitor curae mauris urna mi dolor.</p>

							<form method="post" action="#">
								<div class="row">
									<div class="6u 12u$(mobile)"><input type="text" name="name" placeholder="Name" /></div>
									<div class="6u$ 12u$(mobile)"><input type="text" name="email" placeholder="Email" /></div>
									<div class="12u$">
										<textarea name="message" placeholder="Message"></textarea>
									</div>
									<div class="12u$">
										<input type="submit" value="Send Message" />
									</div>
								</div>
							</form>

						</div>
					</section>
					-->
			</div>

			<div id="footer">

					<ul class="copyright">
						<li>&copy; LeaveRet. All rights reserved.</li><li>Examiner : <!--<a href="http://html5up.net">-->C0mma</a></li>
					</ul>

			</div>

			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>
