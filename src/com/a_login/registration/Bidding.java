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
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

/**
 * A simple {@link android.support.v4.app.Fragment} subclass.
 * 
 */
public class Bidding extends Fragment implements OnClickListener{

	EditText et_product, et_price;
	ImageView img_submit;
	public Bidding() {
		// Required empty public constructor
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		return inflater.inflate(R.layout.fragment_bidding, container, false);
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onActivityCreated(savedInstanceState);
		et_product = (EditText) getActivity().findViewById(R.id.editText_product);
		et_price = (EditText) getActivity().findViewById(R.id.editText_Price);
		img_submit =	 (ImageView) getActivity().findViewById(R.id.imageView_submitbid);
		img_submit.setOnClickListener(this);

	}

	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		System.out.println("inside onclick listener");
		System.out.println("Values Entered : >>>>"+et_product.getText().toString()+et_price.getText().toString());
		if(et_product.getText().length() != 0 && et_price.getText().length() != 0){
			SessionManager session = new SessionManager(getActivity());
			String user = session.getUserName();

			String json = new Gson().toJson(new BidDetails(et_product.getText().toString(), et_price.getText().toString(), user));
			new SubmitBid().execute(json);
			System.out.println("object created");
			Toast.makeText(getActivity().getApplicationContext(), "Your Query has been submitted. Merchants will contact you soon", Toast.LENGTH_LONG).show();

 
		}
		else{
			AlertDialog.Builder alert = new AlertDialog.Builder(getActivity());
			//alert.setTitle(R.string.alert_text);
			alert.setPositiveButton("OK", null);
			if(et_product.getText().length() == 0)
				alert.setMessage(R.string.empty_iwant_query);
			else
				alert.setMessage(R.string.empty_iwant_price);

			AlertDialog dialog = alert.create();
			dialog.show();
		}		
		
	}
	
	/** AsyncTask to check user login */
	private class SubmitBid extends AsyncTask<Object, Void, Object>{

		@Override
		protected Object doInBackground(Object... params) {

			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost("http://54.215.161.157:8989/android/bid");	
			HttpResponse response;
			try{

				httppost.setEntity(new StringEntity((String) params[0]));
				httppost.setHeader("Content-type", "application/json");
				response = httpclient.execute(httppost);
				if(response.getStatusLine().getStatusCode() == 200);
			}catch(Exception e){
				Log.d("Background Task",e.toString());
			}
			return null;
		}
	} 

	private class BidDetails{
		

		private String bid_Query;
		private String bid_Price;
		private String userName;

		public BidDetails(String bid_Query, String bid_Price, String userID) {
			// TODO Auto-generated constructor stub
			super();
			this.bid_Query = bid_Query;
			this.bid_Price = bid_Price;
			this.userName = userID;
		}

		public String getsearch_Query() {
			return bid_Query;
		}
		public String getPrice() {
			return bid_Price;
		}
		public String getUserId() {
			return userName;
		}
	}
}
