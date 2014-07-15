package com.a_login.registration;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import com.google.gson.Gson;

import android.app.AlertDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.view.View.OnClickListener;

/**
 * A simple {@link android.support.v4.app.Fragment} subclass.
 * 
 */
public class IwantResults2 extends Fragment implements OnClickListener {

	 EditText query;
	 EditText price;
	 Button submit;
	 SessionManager session;

	public IwantResults2() {
		// Required empty public constructor
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		session = new SessionManager(getActivity().getApplicationContext());
		return inflater.inflate(R.layout.iwantresulttwo, container, false);
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		
		query = (EditText) getActivity().findViewById(R.id.iwantQuery_editText);
		price = (EditText) getActivity().findViewById(R.id.iwantPrice_editText);
		submit = (Button) getActivity().findViewById(R.id.iwant_button);
		if(submit == null)
			System.out.println("BUTTON NULL >>>>>>>>>>>>>>>>>>");
		//submit.setOnClickListener(new EnterButtonListener());	
		submit.setOnClickListener(this);
		
	}

	public class EnterButtonListener implements OnClickListener{

		@Override
		public void onClick(View arg0) {
			if(query.getText().length() != 0 && price.getText().length() != 0){

				String json = new Gson().toJson(new BidDetails(query.getText().toString(), price.getText().toString(), session.getUserName()));
				new SubmitBid().execute(json);
			}
			else{
				AlertDialog.Builder alert = new AlertDialog.Builder(getActivity());
				//alert.setTitle(R.string.alert_text);
				alert.setPositiveButton("OK", null);
				if(query.getText().length() == 0)
					alert.setMessage(R.string.empty_iwant_query);
				else
					alert.setMessage(R.string.empty_iwant_price);

				AlertDialog dialog = alert.create();
				dialog.show();
			}

		}

	};

	/** AsyncTask to check user login */
	private class SubmitBid extends AsyncTask<Object, Void, Object>{

		@Override
		protected Object doInBackground(Object... params) {

			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost("http://192.168.1.4:8099/Android/bid");	
			HttpResponse response;
			try{

				httppost.setEntity(new StringEntity((String) params[0]));
				httppost.setHeader("Content-type", "application/json");
				System.out.println("!>>>>>>>>>>>>>>>>>");
				response = httpclient.execute(httppost);
				if(response.getStatusLine().getStatusCode() == 200)
					Toast.makeText(getActivity(), "Bid submitted successfully", Toast.LENGTH_SHORT).show();
			}catch(Exception e){
				Log.d("Background Task",e.toString());
			}
			return null;
		}
	} 

	private class BidDetails{
		private String bid_Query;
		private String bid_Price;
		private String userID;

		public BidDetails(String bid_Query, String bid_Price, String userID) {
			super();
			this.bid_Query = bid_Query;
			this.bid_Price = bid_Price;
			this.userID = userID;
		}

		public String getBid_Query() {
			return bid_Query;
		}

		public String getBid_Price() {
			return bid_Price;
		}

		public String getuserID() {
			return userID;
		}


	}

	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		if(query.getText().length() != 0 && price.getText().length() != 0){

			String json = new Gson().toJson(new BidDetails(query.getText().toString(), price.getText().toString(), session.getUserName()));
			new SubmitBid().execute(json);
		}
		else{
			AlertDialog.Builder alert = new AlertDialog.Builder(getActivity());
			//alert.setTitle(R.string.alert_text);
			alert.setPositiveButton("OK", null);
			if(query.getText().length() == 0)
				alert.setMessage(R.string.empty_iwant_query);
			else
				alert.setMessage(R.string.empty_iwant_price);

			AlertDialog dialog = alert.create();
			dialog.show();
		}
	}

}

