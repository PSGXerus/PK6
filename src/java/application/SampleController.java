package application;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;

/**
 * Controller class for the Sample FXML file
 * @author FME
 *
 */
public class SampleController
{
	@FXML
	private Button btn_Back;
	@FXML
	private Button btn_Next;
	@FXML
	private WebView wv_Browser;
	
	/* The web pages that the info screen supports (white list) */
	private final String[] pages = new String[]{"http://www.hm.edu", "http://lsw.ee.hm.edu"};
	
//	private boolean isValid = false;

	/**
     * Initializes the controller class.
	 * This method is called by the FXMLLoader when initialization is complete
	 * */
	@FXML
    public void initialize()
    {		
		/* Initialize web view engine 
		 * For further information about web view and web engine visit https://docs.oracle.com/javafx/2/webview/jfxpub-webview.htm */
		final WebEngine engine = wv_Browser.getEngine();
		/* Load first page */
		engine.load(pages[0]);
				
//		TODO disable buttons when there is no previous or next page
		
		/* Specify action when the back button was pressed */
	    	btn_Back.setOnAction(new EventHandler<ActionEvent>()
	    	{
		    	@Override
		    	public void handle(ActionEvent arg0)
		    	{
//		    		if(checkLocation() == false)
		    			engine.load(pages[0]);
//		    		TODO iterative
		    		
		    	}
		});
	    	
	    	/* Specify action when the next button was pressed */
	    	btn_Next.setOnAction(new EventHandler<ActionEvent>()
	    	{
		    	@Override
		    	public void handle(ActionEvent arg0)
		    	{
//		    		TODO iterative
//		    		if(checkLocation() == false)
		    			engine.load(pages[1]);
		    	}
		});
	}
	
//	private boolean checkLocation()
//	{	
//		/* Check if the current URL is part of the white list */
//		wv_Browser.getEngine().locationProperty().addListener((obs, oldValue, newValue) ->
//		{
//			for(int i=0; i<pages.length; i++)
//    			{
//	    			if(!newValue.equals(pages[i]))
//	    			{	    			
//	    				isValid = true;
//	    				if(oldValue.isEmpty())
//	    				{
//	    					engine.load(pages[i]);
//	    				}
//	    				else
//	    				{
//	    					engine.load(oldValue);
//	    				}
//	    			}
//    			}	
//		});		
//		return isValid;
//	}
}
