package com.a_login.registration;

import java.util.ArrayList;

import globals.Globals;

import org.json.JSONArray;
import org.json.JSONException;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

/**
 * Called from MainActivity to set the list adapter
 * to display overview all messages. On clicking single message
 * it calls DisplayAllMessages to display history chain of the message clicked. 
 * 
 */
public class DisplayMessageList extends Fragment implements OnItemClickListener {

	Globals global;
	JSONArray messagesJSONArray;
	DisplayMessageHistory dmh;
	ArrayList<String> sender_names = new ArrayList<String>();
	ArrayList<String> sender_date = new ArrayList<String>();
	ArrayList<String> sender_message = new ArrayList<String>();
	ArrayList<String> sender_message_id = new ArrayList<String>();
	ListView l;

	public DisplayMessageList() {
		// Required empty public constructor
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		return inflater.inflate(R.layout.layout_display_message_list,
				container, false);
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		try {
			global = Globals.getInstance();
			messagesJSONArray = new JSONArray(global.getMessagesJSONArray());

			for(int i=0; i<messagesJSONArray.length(); i++){
				Log.d("Tesat", "ID >>>>>>"+messagesJSONArray.getJSONObject(i).getString("from_id"));
				sender_names.add(messagesJSONArray.getJSONObject(i).getString("from_id"));
				sender_date.add(messagesJSONArray.getJSONObject(i).getString("date"));
				sender_message.add(messagesJSONArray.getJSONObject(i).getString("message"));
				sender_message_id.add(messagesJSONArray.getJSONObject(i).getString("bidding_id"));
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}

		l = (ListView) getView().findViewById(R.id.display_messages_list);		
		DisplayMessagesAdapter adapter = new DisplayMessagesAdapter(getActivity(), sender_names, sender_date, sender_message);
		l.setAdapter(adapter);
		l.setOnItemClickListener(this);
		l.setEmptyView(getActivity().findViewById(R.id.emptyProductDeals));
	}

	@Override
	public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {			
		Intent intent = new Intent(getActivity(), DisplayAllMessages.class);
		intent.putExtra("msgID", sender_message_id.get(position));
		SessionManager session = new SessionManager(getActivity());
		String user = session.getUserName();
		intent.putExtra("uid", user);
		startActivity(intent);
	}

}

class DisplayMessagesAdapter extends ArrayAdapter<String>{

	Context contex;
	ArrayList<String> sender_name;
	ArrayList<String> sender_date;
	ArrayList<String> sender_message;

	DisplayMessagesAdapter(Context c, ArrayList<String> sender_name, ArrayList<String> sender_date, ArrayList<String> sender_message){
		super(c, R.layout.display_message_single_row, sender_name);
		this.contex = c;
		this.sender_name = sender_name;
		this.sender_date = sender_date;
		this.sender_message = sender_message;
	}

	class MyViewHolder{
		TextView name;
		TextView date;
		TextView message;

		MyViewHolder(View v){
			name = (TextView) v.findViewById(R.id.message_sender_name);
			date = (TextView) v.findViewById(R.id.message_sender_date);
			message = (TextView) v.findViewById(R.id.message_sender_message);
		}

	}

	public View getView(int position, View convertView, ViewGroup parent){

		View root = convertView;
		MyViewHolder holder = null;
		if(root==null)
		{
			LayoutInflater inflater = (LayoutInflater) contex.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			root = inflater.inflate(R.layout.display_message_single_row, parent, false);
			holder = new MyViewHolder(root);
			root.setTag(holder);
		}
		else{
			holder = (MyViewHolder) root.getTag();
		}

		holder.name.setText(sender_name.get(position));
		holder.date.setText(sender_date.get(position));
		holder.message.setText(sender_message.get(position));

		return root;

	}

}
