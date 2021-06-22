<!DOCTYPE html>
<html lang='en'>
    <head>
        <title> Gerard Romero's Portal </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="UTF-8">
        <meta http-equiv="Content-type" content="text/html; charset=UTF-8">
        <script type='text/javascript' src='../../configs/configs.js'></script>
	    <script type="text/javascript" src="lib/index.js"></script>
        <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
	    <script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script>
        <link rel='stylesheet' href='../lib/index.css'>
        <link rel='stylesheet' href='lib/index.css'>
    </head>
    <body onload='init();'>
        <div id='top-nav'>
            <img src='../assets/moon.png' onclick='toggleDarkMode()' id='darkModeButton' alt='darkModeToggler'></img>
            <select id='Lang' onchange="redirect()">
                <option value='es'>Spanish</option>
                <option value='ca'>Catalan</option>
                <option value='en' selected='selected'>English</option>
            </select>
        </div>
        <div id='main'>
            <div id='left-nav' class="sidenav">
                <a href="../index_en.html">───<br>
                            Home<br>
                            ─&#8962;─</a>
                <a href="index_en.php">─────<br>
                            Projects<br>
                            ──&#128736;──</a>
                <a href="#">─────<br>
                            About me<br>
                            ──&#128483;──</a>
                <a href="#">─────<br>
                            Contact<br>
                            ──&#9993;──</a>
            </div>
            <div id='home'>
                <h2>Welcome to my custom pc builder</h2>
                <h3>I strongly recommend selecting from <b>top</b> to <b>bottom</b></h3>
                <div id='content'>
                    <div id='components'>
                        <form action='' method='post'>
                            <input type="submit" id='moboselector' name='moboselector' onclick="javascript:this.parentNode.submit();" value='MOTHERBOARD'></input>
                            <span id='moboselectordisplay'></span>
                            <input type="submit" id='cpuselector'  name='cpuselector'  onclick="javascript:this.parentNode.submit();" value='CPU'></input>
                            <span id='cpuselectordisplay'></span>
                            <input type="submit" id='gpuselector'  name='gpuselector'  onclick="javascript:this.parentNode.submit();" value='GPU'></input>
                            <span id='gpuselectordisplay'></span>
                            <input type="submit" id='ramselector'  name='ramselector'  onclick="javascript:this.parentNode.submit();" value='RAM'></input>
                            <span id='ramselectordisplay'></span>
                            <input type="submit" id='hddselector'  name='hddselector'  onclick="javascript:this.parentNode.submit();" value='HDD'></input>
                            <div id='hddselectordiv'></div>
                            <input type="submit" id='ssdselector'  name='ssdselector'  onclick="javascript:this.parentNode.submit();" value='SSD'></input>
                            <div id='ssdselectordiv'></div>
                            <input type="submit" id='sshdselector' name='sshdselector' onclick="javascript:this.parentNode.submit();" value='SSHD'></input>
                            <div id='sshdselectordiv'></div>
                            <input type="submit" id='m2selector'   name='m2selector'   onclick="javascript:this.parentNode.submit();" value='NVMe M.2'></input>
                            <div id='m2selectordiv'></div>
                            <input type="hidden" name='mobo' value='' id='hiddenmobo'>
                            <input type="hidden" name='cpu'  value='' id='hiddencpu'>
                            <input type="hidden" name='gpu'  value='' id='hiddengpu'>
                            <input type="hidden" name='ram'  value='' id='hiddenram'>
                            <div id='hiddenhdddiv'></div>
                                <!input type="hidden" name='hdd'  value='' id='hiddenhdd'>
                            <div id='hiddenssddiv'></div>
                                <!input type="hidden" name='ssd'  value='' id='hiddenssd'>
                            <div id='hiddensshddiv'></div>
                                <!input type="hidden" name='sshd' value='' id='hiddensshd'>
                            <div id='hiddenm2div'></div>
                                <!input type="hidden" name='m2'   value='' id='hiddenm2'>
                        </form>
                    </div>
                    <div id='Info'>
                        <div id='scheme'>
                            <div id='motherboard' class='onlymobo'>
                                <div id='cpu'></div>
                                <div id='gpu'>
                                    <div id='pcie1'></div>
                                    <div id='pcie2'></div>
                                    <div id='pcie3'></div>
                                    <div id='pcie4'></div>
                                </div>
                                <div id='ram'>
                                    <div id='ram1'></div>
                                    <div id='ram2'></div>
                                    <div id='ram3'></div>
                                    <div id='ram4'></div>
                                </div>
                            </div>
                            <div id='storage'>
                                <img id='hdd' alt='Hard Disk Drive' src='../assets/hdd.png'></img>
                                <img id='ssd' alt='Hybrid Drive' src='../assets/sshd.png'></img>
                                <img id='sshd' alt='Solid State Drive' src='../assets/ssd.png'></img>
                                <img id='m2' alt='Non Volatile Memory express' src='../assets/nvme.png'></img>
                            </div>
                        </div>
                        <div id='detailed'>
                            <div id='motherboardInfo'>
                                <h2>Motherboard</h2>
                                <p>The main connector for all components</p>
                            </div>
                            <div id='cpuInfo'>
                                <h2>CPU</h2>
                                <p>A central processing unit (CPU) is the electronic circuitry that executes instructions comprising a computer program. The CPU performs basic arithmetic, logic, controlling, and input/output (I/O) operations specified by the instructions in the program</p>
                            </div>
                            <div id='gpuInfo'>
                                <h2>GPU</h2>
                                <p>Graphics processing unit, a specialized processor originally designed to accelerate graphics rendering. GPUs can process many pieces of data simultaneously, making them useful for machine learning, video editing, and gaming applications</p>
                            </div>
                            <div id='ramInfo'>
                                <h2>RAM</h2>
                                <p>RAM is short for “random access memory” and while it might sound mysterious, RAM is one of the most fundamental elements of computing. RAM is the super-fast and temporary data storage space that a computer needs to access right now or in the next few moments</p>
                            </div>
                            <div id='hddInfo'>
                                <h2>HDD</h2>
                                <p>Memory for your files, slow but long life expectancy. Suited for storing important files, programs and videogames</p>
                            </div>
                            <div id='sshdInfo'>
                                <h2>SSHD</h2>
                                <p>Not as fast as an SSD and not as long-lived as an HDD, but a middlepoint</p>
                            </div>
                            <div id='ssdInfo'>
                                <h2>SSD</h2>
                                <p>Super fast memory storage but might wear faster than a Hard Disk Drive. Not suited for important file storing but programs that waste a lot of your time booting/loading</p>
                            </div>
                            <div id='m2Info'>
                                <h2>NVMe (M.2)</h2>
                                <p>A Solid State Drive directly connected to your motherboard. Even faster than a traditional SSD for long read/write operations like OS booting, file transfer or game booting and as long lasted as an SSD</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id='table'>
            <?php include 'lib/test.php' ;?>
        </div>
    </body>
</html>