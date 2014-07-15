package com.a_login.registration;


import java.util.ArrayList;
import java.util.HashMap;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import com.google.gson.Gson;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Registration extends Activity implements OnClickListener{
	EditText firstName,lastName,password,emailId;
	Button submit, reset;
	boolean isRegistered = false;
	


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_registration);
		firstName = (EditText) findViewById(R.id.edit_firstname);
		lastName = (EditText) findViewById(R.id.edit_lastname);
		password = (EditText) findViewById(R.id.edit_pass);
		emailId = (EditText) findViewById(R.id.edit_email);
		submit = (Button) findViewById(R.id.button_submit);
		reset = (Button) findViewById(R.id.button_reset);
submit.setOnClickListener(this);
	}

	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		if(v == submit){
			postLoginData();
			Log.d("Sagar","inside submit");
		}
	}

	private void postLoginData() {
		// TODO Auto-generated method stub


		String strFirstName = firstName.getText().toString();
		String strLastname = lastName.getText().toString();
		String strPassword = password.getText().toString();
		String stremail = emailId.getText().toString();

		Gson gson = new Gson();
		String json = gson.toJson(new RegistrationData(strFirstName,strLastname,stremail,strPassword));
		//change to registration url
		String url = "http://54.215.161.157:8989/Android/Signup";
		Log.d("Sagar","Sending Data");
		new SendData().execute(url, json);

	}

	private class RegistrationData{
		String strFirstName, strLastname,stremail, strPassword ;
		public RegistrationData(String strFirstName, String strLastname,
				String stremail, String strPassword) {
			// TODO Auto-generated constructor stub
			this.strFirstName=strFirstName;
			this.strLastname = strLastname;
			this.stremail = stremail;
			this.strPassword = strPassword;
		}
		public String getStrFirstName() {
			return strFirstName;
		}
		public String getStrLastname() {
			return strLastname;
		}
		public String getStremail() {
			return stremail;
		}
		public String getStrPassword() {
			return strPassword;
		}

	}
	private class SendData extends AsyncTask<String, Integer, String>{

		@Override
		protected String doInBackground(String... params) {
			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(params[0]);
			HttpResponse response;

			try {
				httppost.setEntity(new StringEntity(params[1]));
				httppost.setHeader("Content-type", "application/json");
				response = httpclient.execute(httppost);
				//Log.d("Sagar",EntityUtils.toString(response.getEntity()));

				isRegistered = new JSONObject(EntityUtils.toString(response.getEntity())).getBoolean("Signup_status");
				Log.d("Sagar","isRegistered >>> "+isRegistered);
			}catch(Exception e){
				isRegistered = false;
			}
			return null;
		}
		
		@Override
		protected void onPostExecute(String result) {
			if(isRegistered){
				Intent i = new Intent(getApplicationContext(), LoginActivity.class);
				startActivity(i);
				finish();				
			}
			else{
				Toast.makeText(Registration.this, "Registration Failed", Toast.LENGTH_SHORT).show();
			}
		}
	}
}
