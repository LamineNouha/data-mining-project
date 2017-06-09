<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>

<title>HEART DOCTOR</title>
<meta name="keywords" content="#" />
<meta name="description" content="#" />
<link href="style.css" rel="stylesheet" type="text/css" />

<link rel="stylesheet" type="text/css" href="stylesheet/styles.css" />

<script language="javascript" type="text/javascript" src="script/newyorklasik-1.2.1-core.js"></script>
<script language="javascript" type="text/javascript" src="script/newyorklasik-1.2-more.js"></script>
<script language="javascript" type="text/javascript" src="script/newyorklasik-1.1.js"></script>
<script language="javascript" type="text/javascript">
	window.addEvents({
		'domready': function(){
			/* thumbnails example , div containers */
			new newyorklasik({
						overallContainer: 'newyorklasik_outer',
						elementScrolled: 'newyorklasik_inner',
						thumbsContainer: 'newyorklasik_items',		
						itemsVisible: 5,
						elemsSlide: 2,
						duration: 150,
						itemsSelector: '.newyorklasik_element',
						itemWidth: 158,
						showControls:1});
		},
		
	});
</script>


<script language="javascript" type="text/javascript">
function clearText(field)
{
    if (field.defaultValue == field.value) field.value = '';
    else if (field.value == '') field.value = field.defaultValue;
}



	


</script>
</head>
<body>
<div id="site_title_bar_wrapper_outter">
<div id="site_title_bar_wrapper_inner">

	<div id="site_title_bar">
    
    	<div id="banner_left">
    	
		    
            
  
         <form action="MyServlet" method="get">
            <div id="menu">
            
              <ul>
                    <li><a href="#
" class="current"><span></span><input style="margin-top:-1px" size="17" type="text" name="temperature" placeholder="Temperature"/></a></li>
                    <li><a  class="current" href="#" target="_parent"><span></span><input style="margin-top:-1px" size="17" type="text" name="battement" placeholder="Heart Beatting"/></a></li>
                    <li><a href="#" class="current"
" ><span></span><input style="margin-top:-1px" size="17" type="text" name="tension" placeholder="Blood pressure"/></a></li>
                    
                </ul>     	
            </div> <!-- end of menu -->
            
             <div id="banner_right" style="margin-left:340px;margin-top:-280px">
            <div id="banner_box">
           
           
           
           		<h1>Alert </h1>
                <p>In this case when Temperature: <c:catch var="exception1">${requestScope.temperature}</c:catch> ,Heart beatting: <c:catch var="exception2">${requestScope.battement}</c:catch> and Blood Pressure: <c:catch var="exception3">${requestScope.tension}</c:catch>, will we raise an alert ? <br />
                &nbsp;</p>
                <c:catch var="exception">${requestScope.alert}</c:catch>
				

				
              <div class="button" ><input type="submit" value="see"></div>
           <br><br>
            </div>
		</div>
		</form>
  
		</div>
            
    </div> <!-- end of site_title_bar  -->
    
</div> <!-- end of site_title_bar_wrapper_inner -->
</div> <!-- end of site_title_bar_wrapper_outter  -->

<div id="content">

	<div class="section_w940">
    	<p class="em_text"></p>
        
      <p></p>
        
  </div>
    
   
    
 <!-- end of product gallery -->

    
</div> <!-- end of content -->

<div id="footer_wrapper">

	<div id="footer">
    
    
    	
     
      
        <div class="cleaner_h40"></div>

        <center>
        	Copyright © 2017<a href="#
">INSAT GL4 </a> | 
           Data Mining
        </center>
		<p>
   
  </p>

    
    </div> <!-- end of footer -->

	<div class="cleaner"></div>
</div> <!-- end of footer wrapper -->





</body>
</html>