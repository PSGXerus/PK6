package application;

import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.VBox;
import javafx.fxml.FXMLLoader;

/**
 * Main class of the info screen GUI 
 * @author FME
 *
 */
public class Main extends Application
{
	/**
	 * @param primaryStage - the main stage of the application
	 */
	@Override
	public void start(Stage primaryStage)
	{
		try 
		{
			VBox root = (VBox)FXMLLoader.load(getClass().getResource("Sample.fxml"));
			Scene scene = new Scene(root,600,400);
			scene.getStylesheets().add(getClass().getResource("application.css").toExternalForm());
			primaryStage.setScene(scene);
			primaryStage.setTitle("Infoscreen");
//			primaryStage.setFullScreen(true);
			primaryStage.show();
		} 
		catch(Exception e) 
		{
			/* Print to terminal */
			System.err.println(e.getMessage());
		}
	}

	/**
	 * Launch application
	 * @param args
	 */
	public static void main(String[] args) 
	{
		launch(args);
	}
}
