package com.a_login.registration;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;

import globals.Globals;
import android.support.v4.app.FragmentActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;
import java.util.Locale;

import org.json.JSONException;
import org.json.JSONObject;


import android.support.v7.app.ActionBarActivity;

import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.view.Menu;
import android.widget.TextView;


public class Notification extends  FragmentActivity  {
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_notification);
		SessionManager session = new SessionManager(getApplicationContext());
String user = session.getUserName();
String url = "http://54.215.161.157:8989/Android/ViewMessage/"+user;
		
		new GetMessageFromServer().execute(url);

	}

	private class GetMessageFromServer extends AsyncTask<String, String, String>{
		@Override
		protected String doInBackground(String... params) {
			try{
				URL messages = new URL(params[0]);

				JSONObject messagesJSON = new JSONObject(getResponse(messages).toString());
				
				if(messagesJSON!=null){
					Globals globals = Globals.getInstance();
					globals.setMessagesJSONArray(messagesJSON.getJSONArray("messages").toString());
				}
			}catch(IOException e){
				Log.d("Test", "IOException", e);
			} catch (JSONException e) {
				Log.d("Test", "JSONException", e);
			}

			return null;

		}
        
        @Override
        protected void onPostExecute(String result) {
			getSupportFragmentManager().beginTransaction().add(R.id.container1, new DisplayMessageList()).commit();
			
        }
	}
	


	public StringBuilder getResponse(URL url){
		StringBuilder responseStrBuilder = null;
		try{
			URLConnection connection = url.openConnection();

			HttpURLConnection httpConnection = (HttpURLConnection) connection;
			Log.d("2", "Inside 2 >>>>>>");

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
			Log.d("Sagar", "IOException", e);
		}
		return responseStrBuilder;
	}
}