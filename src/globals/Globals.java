package globals;

import java.util.ArrayList;

public class Globals{
	private static Globals instance;

	// Global variable
	// Global variable
		private String messagesJSONArray;
		private String messageHistoryJSON;
		private String localDealsJSONArray;

	private ArrayList<String> name;
	private ArrayList<String> thumbnailImage;
	private ArrayList<String> shortDescription;

	// Restrict the constructor from being instantiated
	private Globals(){}


	public static synchronized Globals getInstance(){
		if(instance==null){
			instance=new Globals();
		}
		return instance;
	}
	
	public ArrayList<String> getName() {
		return name;
	}


	public void setName(ArrayList<String> name) {
		this.name = name;
	}


	public ArrayList<String> getThumbnailImage() {
		return thumbnailImage;
	}


	public void setThumbnailImage(ArrayList<String> thumbnailImage) {
		this.thumbnailImage = thumbnailImage;
	}


	public ArrayList<String> getShortDescription() {
		return shortDescription;
	}


	public void setShortDescription(ArrayList<String> shortDescription) {
		this.shortDescription = shortDescription;
	}


	
	
	public String getMessageHistoryJSON() {
		return messageHistoryJSON;
	}


	public void setMessageHistoryJSON(String messageHistoryJSON) {
		this.messageHistoryJSON = messageHistoryJSON;
	}


	public String getMessagesJSONArray() {
		return messagesJSONArray;
	}


	public void setMessagesJSONArray(String messagesJSONArray) {
		this.messagesJSONArray = messagesJSONArray;
	}

	
}