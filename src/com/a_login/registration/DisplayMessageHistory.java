package com.a_login.registration;

import globals.Globals;

import java.io.IOException;
import java.util.ArrayList;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;

import com.google.gson.Gson;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.Toast;
import android.widget.LinearLayout.LayoutParams;

public class DisplayMessageHistory extends Fragment implements OnClickListener{

	ArrayList<String> sender_names = new ArrayList<String>();
	ArrayList<String> sender_date = new ArrayList<String>();
	ArrayList<String> sender_message = new ArrayList<String>();
	JSONArray messageHistoryJSONArray;
	ListView l;
	Globals global;
	String currentBidID;

	public DisplayMessageHistory() {
		// Required empty public constructor
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {

		currentBidID = this.getArguments().getString("bid_id");
		return inflater.inflate(R.layout.amessagehis,
				container, false);
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		try {
			global = Globals.getInstance();
			messageHistoryJSONArray = new JSONArray(global.getMessageHistoryJSON());
			for(int i=0; i<messageHistoryJSONArray.length(); i++){
				sender_names.add(messageHistoryJSONArray.getJSONObject(i).getString("From_id"));
				sender_date.add(messageHistoryJSONArray.getJSONObject(i).getString("date"));
				sender_message.add(messageHistoryJSONArray.getJSONObject(i).getString("Description"));	
			}
		} catch (JSONException e) {
			Log.d("DisplayMessageHistory", "IOException", e);
		}

		l = (ListView) getView().findViewById(R.id.listView_amaghis);		
		DisplayMessagesAdapter adapter = new DisplayMessagesAdapter(getActivity(), sender_names, sender_date, sender_message);
		l.setAdapter(adapter);
		LinearLayout ll = (LinearLayout) getView().findViewById(R.id.ll_messagehis);
		Button button = new Button(getActivity(), null, android.R.attr.buttonStyleSmall);
		LinearLayout.LayoutParams dimensions = new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT);
		button.setLayoutParams(dimensions);
		button.setText("Make new bid");
		button.setOnClickListener(this);
		ll.addView(button);

		/*l.setOnItemClickListener(this);
		l.setEmptyView(getActivity().findViewById(R.id.emptyProductDeals));*/
	}

	@Override
	public void onClick(View v) {

		final EditText bidMsgText = new EditText(getActivity());
		LinearLayout.LayoutParams dimensions = new LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT);
		bidMsgText.setLayoutParams(dimensions);
		bidMsgText.requestFocus();
		bidMsgText.setSingleLine(false);
		bidMsgText.setImeOptions(EditorInfo.IME_FLAG_NO_ENTER_ACTION);
		bidMsgText.setEms(10);
		
		final EditText bidPriceText = new EditText(getActivity());
		bidPriceText.setLayoutParams(dimensions);
		bidPriceText.setEms(10);
		
		final LinearLayout ll = (LinearLayout) v.getParent();
		ll.addView(bidMsgText);
		ll.addView(bidPriceText);

		Button button = new Button(getActivity(), null, android.R.attr.buttonStyleSmall);
		button.setLayoutParams(dimensions);
		button.setText("Post bid");
		button.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) { 

				// Add your data
				Gson gson = new Gson();
				SessionManager session = new SessionManager(getActivity());
				String user = session.getUserName();
				String json = gson.toJson(new PostData(currentBidID, user, bidMsgText.getText().toString(), bidPriceText.getText().toString()));
				String url = "http://54.215.161.157:8989/Android/MessageList";
				new SendData().execute(url, json);
			}
		});
		ll.addView(button);
		ll.removeView(v);

	}	

	private class SendData extends AsyncTask<String, String, String>{
		@Override
		protected String doInBackground(String... params) {

			HttpClient httpclient = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(params[0]);

			try {
				httppost.setEntity(new StringEntity(params[1]));
				httppost.setHeader("Content-type", "application/json");

				// Execute HTTP Post Request
				/*   ResponseHandler responseHandler = new BasicResponseHandler();
			    return httpclient.execute(httppost, responseHandler);*/
				httpclient.execute(httppost);

			} catch (ClientProtocolException e) {
				// TODO Auto-generated catch block
			} catch (IOException e) {
				// TODO Auto-generated catch block
			}	
			return null;
		}
		
		@Override
		protected void onPostExecute(String result) {
			Toast.makeText(getActivity(), "Your new bid has been submitted", Toast.LENGTH_SHORT).show();
		}
	}

	public class PostData{
		String bid_id;
		String user_name;
		String bid_data;
		String bid_price;

		PostData(String bid_id, String user_name, String bid_data, String bid_price){
			this.bid_id = bid_id;
			this.user_name = user_name;
			this.bid_data = bid_data;
			this.bid_price = bid_price;
		}
	}

}