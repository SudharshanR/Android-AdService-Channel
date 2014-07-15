package com.a_login.registration;

import globals.Globals;
import globals.ProductsList;
import globals.ImgDetails;

import java.util.ArrayList;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import bean.Product;
import adapter.ProductAdapter;

import com.google.gson.Gson;
import com.nostra13.universalimageloader.core.ImageLoader;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;

public class Iwantscreen3 extends Fragment implements OnClickListener, OnItemClickListener {

	ListView mListView;
	JSONArray deals;
	Globals global;
	ArrayList<Product> mProductList = new ArrayList<Product>();
	ArrayList<String> titles = new ArrayList<String>();
	ArrayList<Double> prices = new ArrayList<Double>();
	ArrayList<String> desc = new ArrayList<String>();
	ArrayList<String> images = new ArrayList<String>();
	ArrayList<Bitmap> bitmapImages = new ArrayList<Bitmap>();
	ProgressBar progress;
	ImageLoader image;
	Button btn_send;
	EditText searchQuery;
	ProductsList productsList;
	OnListItemSelected mCallback;

	public Iwantscreen3() {
		// Required empty public constructor
	}

	// Container Activity must implement this interface
    public interface OnListItemSelected {
        //public void onProductSelected(ImageDetails imgDetails);
    	public void onProductSelected(int position);
    }
    
    @Override
    public void onAttach(Activity activity) {
    	super.onAttach(activity);
    	try {
            mCallback = (OnListItemSelected) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement OnHeadlineSelectedListener");
        }
    }
    
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		View view = inflater.inflate(R.layout.iwant3,container, false);

		if(!(savedInstanceState == null)){
			titles = savedInstanceState.getStringArrayList("titles");
			desc = savedInstanceState.getStringArrayList("desc");
			bitmapImages = savedInstanceState.getParcelableArrayList("bitmapImages");
		}

		return view;
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		productsList = ProductsList.getInstance();
		btn_send = (Button) getActivity().findViewById(R.id.btn_iwant3send);
		mListView = (ListView) getActivity().findViewById(R.id.lv_countries);
		progress = (ProgressBar) getActivity().findViewById(R.id.imgProgress);
		searchQuery = (EditText) getActivity().findViewById(R.id.editText_iwantquery);
		btn_send.setOnClickListener(this);
	}

	@Override
	public void onClick(View arg0) {
		System.out.println("Sud >>> Button Cliciked");
		DownloadTask downloadTask = new DownloadTask();
		downloadTask.execute();        
		mListView.setOnItemClickListener(this);
	}

	/** AsyncTask to download json data */
	private class DownloadTask extends AsyncTask<String, Integer, String>{
		String data = null;
		String json = new Gson().toJson(new BidDetails(searchQuery.getText().toString()));

		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost("http://54.215.161.157:8989/searchproduct");	
		HttpResponse response;
		
		@Override
		protected void onPreExecute() {
			// TODO Auto-generated method stub
			super.onPreExecute();
			progress.setVisibility(View.VISIBLE);
		}

		@SuppressLint("NewApi")
		@Override
		protected String doInBackground(String... url) {
			try{
				StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
				StrictMode.setThreadPolicy(policy); 
				httppost.setEntity(new StringEntity((String) json));
				httppost.setHeader("Content-type", "application/json");
				response = httpclient.execute(httppost);
				data =EntityUtils.toString(response.getEntity());
			}catch(Exception e){
				Log.d("Background Task",e.toString());
			}
			return data;
		}

		@SuppressLint("NewApi")
		@Override
		protected void onPostExecute(String result) {
			// The parsing of the xml data is done in a non-ui thread 
			ListViewLoaderTask listViewLoaderTask = new ListViewLoaderTask();
			listViewLoaderTask.execute(result);                        
		}
	}

	/** AsyncTask to parse json data and load ListView */
	private class ListViewLoaderTask extends AsyncTask<String, String, String>{

		JSONArray jArray; 
		@SuppressLint("NewApi")
		@Override
		protected String doInBackground(String... strJson) {
			try{
				//jObject = new JSONObject(strJson[0]);
				//jString = jObject.getJSONArray("products").toString();
				//jArray = new JSONArray(new JSONObject(strJson[0]).getJSONArray("products").toString());
				jArray = new JSONObject(strJson[0]).getJSONArray("products");
				Log.d("Sagar","JSON Array >>>>>"+jArray.toString());

				for(int i=0;i<jArray.length();i++){
					titles.add(jArray.getJSONObject(i).getString("name"));
					prices.add(jArray.getJSONObject(i).getDouble("price"));
					desc.add(jArray.getJSONObject(i).getString("description"));
					images.add(jArray.getJSONObject(i).getString("image"));
				}

			}catch(Exception e){
				Log.d("JSON Exception1",e.toString());
			}	  
			return null;
		}

		/** Invoked by the Android on "doInBackground" is executed */
		@SuppressWarnings("unchecked")
		@Override
		protected void onPostExecute(String result) {
			ImageLoaderTask imgLoader = new ImageLoaderTask();
			imgLoader.execute(images);
		}		
	}

	/** AsyncTask to download and load an image in ListView */
	private class ImageLoaderTask extends AsyncTask<ArrayList<String>, Void, ArrayList<Bitmap>>{

		@Override
		protected ArrayList<Bitmap> doInBackground(ArrayList<String>... imagesList) {
			image = ImageLoader.getInstance();
			for(int i=0;i<imagesList[0].size();i++){
				bitmapImages.add(image.loadImageSync(imagesList[0].get(i)));
				mProductList.add(new Product(titles.get(i), desc.get(i), prices.get(i), bitmapImages.get(i)));
			}

			return bitmapImages;
		}

		@Override
		protected void onPostExecute(ArrayList<Bitmap> bitmapList) {
			//CustomAdapter adapter = new CustomAdapter(getActivity(), titles, bitmapList, desc);
			// Setting adapter for the listview
			productsList.setProducts(mProductList);
			progress.setVisibility(View.GONE);
			mListView.setAdapter(new ProductAdapter(mProductList, LayoutInflater.from(getActivity()), false));
		}
	}

	@SuppressLint("NewApi")
	@Override
	public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
		//mCallback.onProductSelected(new ImageDetails(titles.get(position), desc.get(position), bitmapImages.get(position)));
		mCallback.onProductSelected(position);
	}

	private class BidDetails{
		private String query;

		public BidDetails(String query) {
			super();
			this.query = query;
		}

		public String getsearch_Query() {
			return query;
		}
	}
}

/*class CustomAdapter extends ArrayAdapter<String>{

	Context contex;
	ArrayList<Bitmap> imgs;
	ArrayList<String> titles;
	ArrayList<String> description;

	
	 * Create a constructor which calls super(). In super(), we pass context, the singlerow.xml file, and the datasource
	 
	CustomAdapter(Context c, ArrayList<String> titles, ArrayList<Bitmap> imgs, ArrayList<String> description){
		super(c, R.layout.iwant3_singlerow, titles);
		this.contex = c;
		this.imgs = imgs;
		this.titles = titles;
		this.description = description;
	}

	class MyViewHolder{
		ImageView img;
		TextView title;
		TextView desc;

		MyViewHolder(View v){
			img = (ImageView) v.findViewById(R.id.iv_flag);
			title = (TextView) v.findViewById(R.id.tv_country);
			desc = (TextView) v.findViewById(R.id.tv_country_details);
		}

	}

	public View getView(int position, View convertView, ViewGroup parent){

		View root = convertView;
		MyViewHolder holder = null;

		if(root==null)
		{
			LayoutInflater inflater = (LayoutInflater) contex.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
			root = inflater.inflate(R.layout.iwant3_singlerow, parent, false);
			holder = new MyViewHolder(root);
			root.setTag(holder);
		}
		else{
			holder = (MyViewHolder) root.getTag();
		}

		//holder.img.setImageResource(imgs.get(position));
		holder.img.setImageBitmap(imgs.get(position));
		holder.title.setText(titles.get(position));
		holder.desc.setText(description.get(position));

		return root;

	}

}*/