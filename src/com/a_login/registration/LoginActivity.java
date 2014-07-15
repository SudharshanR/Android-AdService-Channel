package com.a_login.registration;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.HttpResponse;
import org.apache.http.ParseException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import com.google.gson.Gson;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Resources;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity {

	// Email, password edittext
	EditText txtUsername, txtPassword;

	// login button
	Button btnLogin;
	Button btnreg;
	
	String username;
	String password;

	// Alert Dialog Manager
	AlertDialogManager alert = new AlertDialogManager();

	// Session Manager Class
	SessionManager session;
	
	boolean isLoggedIn = false;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_login); 

		// Session Manager
		session = new SessionManager(getApplicationContext());                
		//Resources resource = getResources();
		//String logInUrl = resource.getString(R.string.URL_Login);
		// Email, Password input text
		txtUsername = (EditText) findViewById(R.id.txtUsername);
		txtPassword = (EditText) findViewById(R.id.txtPassword); 

		//Toast.makeText(getApplicationContext(), "User Login Status: " + session.isLoggedIn(), Toast.LENGTH_LONG).show();


		// Login button
		btnLogin = (Button) findViewById(R.id.btnLogin);
		btnreg = (Button) findViewById(R.id.button_Registration);
// for registration
		btnreg.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
				Intent myIntent = new Intent(LoginActivity.this, Registration.class);
				startActivity(myIntent);
			}
		});
			
			
		
		// Login button click event
		btnLogin.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View arg0) {
				// Get username, password from EditText
				username = txtUsername.getText().toString();
				password = txtPassword.getText().toString();

				// Check if username, password is filled				
				if(username.trim().length() > 0 && password.trim().length() > 0){

					Gson gson = new Gson();
					String json = gson.toJson(new LoginInfo(username, password));
					new CheckLogin().execute(json);			
				}else{
					// user didn't entered username or password
					// Show alert asking him to enter the details
					alert.showAlertDialog(LoginActivity.this, "Login failed..", "Please enter username and password", false);
				}

			}
		});
	}  

	/** AsyncTask to check user login */
	private class CheckLogin extends AsyncTask<String, Integer, String>{	
		HttpResponse response;
		
		@Override

		protected String doInBackground(String... params) {
			// check the log in URL before running.
			String  logInUrl ="http://54.215.161.157:8989/Android/Login";
			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(logInUrl);
			try{
				httppost.setEntity(new StringEntity(params[0]));
				Log.d("Sagar","1");

				httppost.setHeader("Content-type", "application/json");
				Log.d("Sagar","2");
				response = httpclient.execute(httppost);
				
				//if(response.getStatusLine()==)
				//JSONObject j1;
				//j1 = new JSONObject(EntityUtils.toString(response.getEntity()));
				
			//	Log.d("Sagar","5");
				isLoggedIn = new JSONObject(EntityUtils.toString(response.getEntity())).getBoolean("status");
				//JSONObject json = new JSONObject(EntityUtils.toString(response.getEntity()));
				//json.keys()
				Log.d("Sagar","Test");
			}catch(Exception e){
				isLoggedIn = false;
				Log.d("Background Task",e.toString());
			}
			return null;
		}
		
		@Override
		protected void onPostExecute(String result) {

			if(isLoggedIn){

				// Creating user login session
				session.createLoginSession(username, password);
				System.out.println("Logged in >>>>>>>>>>>>>>"+username+password);
				// Staring MainActivity
				Intent i = new Intent(getApplicationContext(), MainActivity.class);
				startActivity(i);
				finish();

			}else{
				// username / password doesn't match
				alert.showAlertDialog(LoginActivity.this, "Login failed..", "Username/Password is incorrect", false);
			}	
			
		}
	} 
	
	private class LoginInfo{
		private String username;
		private String password;
		
		public LoginInfo(String userName, String password) {
			this.username = userName;
			this.password = password;
		}
		
		public String getUserName() {
			return username;
		}
		public String getPassword() {
			return password;
		}
		
	}
}