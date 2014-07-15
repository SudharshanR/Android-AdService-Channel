package com.a_login.registration;

import globals.Globals;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;

import org.json.JSONException;
import org.json.JSONObject;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;

public class DisplayAllMessages extends FragmentActivity {

	String mID;
	String uID;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_display_all_messages);

		Intent intent = getIntent();
		mID = intent.getStringExtra("msgID");
		uID = intent.getStringExtra("uid");

		String url = "http://54.215.161.157:8989/Android/MessageList/"+uID+"/"+mID;
		Log.d("Test", ">>>>>>>>>>>"+url);
		new GetMessageHistory().execute(url);
	}


	private class GetMessageHistory extends AsyncTask<String, String, String>{
		@Override
		protected String doInBackground(String... params) {
			String response = null;
			JSONObject messageJSON = null;
			URL messages = null;
			try{
				messages = new URL(params[0]);
				response = getResponse(messages).toString();
				System.out.println("Main RESPNSE >>>>>>>>>>"+response);
			}catch(IOException e){
				//To handle socket exception which occurs upon frequent requests
				response = getResponse(messages).toString();
				System.out.println("Exception RESPNSE >>>>>>>>>>"+response);
				Log.d("GetMessageHistory", "IOException", e);
			}
			
			try{
				messageJSON = new JSONObject(response);

				if(messageJSON!=null){
					System.out.println("Setting messages >>>>>>>>>>");
					Globals globals = Globals.getInstance();
					globals.setMessageHistoryJSON(messageJSON.getJSONArray("messages").toString());
				}
			}catch (JSONException e) {
				Log.d("GetMessageHistory", "JSONException", e);
			}

			return null;

		}

		@Override
		protected void onPostExecute(String result) {
			Bundle bundle = new Bundle();
			bundle.putString("bid_id", mID);
			DisplayMessageHistory dmh = new DisplayMessageHistory();
			dmh.setArguments(bundle); 
			System.out.println("Before loading container>>>>>>>>>>>>>>>>>>>");
			getSupportFragmentManager().beginTransaction().add(R.id.container1, dmh).commit();
		}
	}

	public StringBuilder getResponse(URL url){
		StringBuilder responseStrBuilder = null;
		try{
			URLConnection connection = url.openConnection();

			HttpURLConnection httpConnection = (HttpURLConnection) connection;
			int responseCode = httpConnection.getResponseCode();

			if(responseCode == HttpURLConnection.HTTP_OK){
				InputStream ip = httpConnection.getInputStream();
				BufferedReader streamReader = new BufferedReader(new InputStreamReader(ip)); 
				responseStrBuilder = new StringBuilder();
				String inputStr;

				while ((inputStr = streamReader.readLine()) != null){
					responseStrBuilder.append(inputStr);
				}
			}
		}catch(IOException e){
			Log.d("GetMessageHistory", "IOException", e);
		}
		return responseStrBuilder;
	}

}

