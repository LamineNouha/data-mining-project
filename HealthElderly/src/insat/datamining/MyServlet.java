package insat.datamining;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.RandomAccessFile;
import java.io.StringWriter;
import java.nio.charset.Charset;

import org.python.util.PythonInterpreter;


import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.python.util.PythonInterpreter;

/**
 * Servlet implementation class MyServlet
 */

public class MyServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;

    /**
     * Default constructor. 
     */
    public MyServlet() {
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
	//	System.out.println("nooooohhhhh");
		String a =request.getParameter("temperature");  
		String b =request.getParameter("battement");  
		String c =request.getParameter("tension");  
		
		
		String abc = a+","+b+","+c;
		//String abc = "37.7,65.2,16";
		System.out.println(abc);
		
		String[] arguments = {"C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/alg.py","C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/BA.csv",abc,"--decide" };
		PythonInterpreter.initialize(System.getProperties(), System.getProperties(), arguments);
		org.python.util.PythonInterpreter python = new org.python.util.PythonInterpreter();
		StringWriter out = new StringWriter();
		python.setOut(out);
		python.execfile("C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/alg.py");
		String outputStr = out.toString();
		System.out.println(outputStr);
		try{
			File ff=new File("C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/ttt.txt"); // définir l'arborescence
			ff.createNewFile();
			FileWriter ffw=new FileWriter(ff);
			ffw.write(outputStr);  // écrire une ligne dans le fichier resultat.txt
			//ffw.write("/n"); // forcer le passage à la ligne
			ffw.close(); // fermer le fichier à la fin des traitements
			} catch (Exception e) {}
		
		
		/*
		
		String pythonScriptPath = "C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/alg.py";
		String[] cmd = new String[6];
		cmd[0] = "python";
		cmd[1] = pythonScriptPath;
		cmd[2] = "C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/BA.csv";
		cmd[3] ="37.7,65.2,16";
		cmd[4] ="--decide";
		cmd[5]="> C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/ttt.txt";
		Runtime rt = Runtime.getRuntime();
		Process pr = rt.exec(cmd);
		
		ProcessBuilder builder = new  ProcessBuilder(cmd.toString(), "/c", "C://Users//User//Downloads//program.exe", "C://Users//User//Downloads//file.txt" , "5");
		builder.redirectOutput(new File("C://Users//User//Downloads//result.txt"));
		builder.redirectError(new File("C://Users//User//Downloads//resulterr.txt"));

		Process p = builder.start(); // throws IOException*/
		
		
		String line;
		try (
		    InputStream fis = new FileInputStream("C:/Users/nouha/Desktop/S2/datamining/projet/decisiontrees-master/ttt.txt");
		    InputStreamReader isr = new InputStreamReader(fis, Charset.forName("UTF-8"));
		    BufferedReader br = new BufferedReader(isr);
		) {
		    while ((line = br.readLine()) != null) {
		        // Deal with  the line
		    	  
		    	  System.out.print(line);
		    	  
		    	  request.setAttribute("alert",line);
		    	  
		    }
		
		}
	    
		
		request.setAttribute("temperature",a);  
		request.setAttribute("battement",b);  
		request.setAttribute("tension",c); 
	    
		
		
		request.getRequestDispatcher("index.jsp").forward(request, response);
		 
	}

}
