package com.a_login.registration;

import java.io.InputStream;
import java.net.URL;

import de.greenrobot.event.EventBus;
import android.os.Bundle;
import android.os.StrictMode;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.view.Menu;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class SingleProductActivity extends Activity {
	TextView tv1;
	TextView tv2;
	TextView tv3;
	Button addToCart;
	Button checkOut;
	Button viewCart;
	ImageView imgv;
	String imageLocation;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		System.out.println("Sagar>>> from single item>>>>>>>>>>");

		setContentView(R.layout.activity_single_product);
		tv1 = (TextView) findViewById(R.id.textV_SPAdesc);
		tv3 = (TextView) findViewById(R.id.textV_SPAtitle);
		imgv = (ImageView) findViewById(R.id.imageV_SPAimage);
		EventBus bus2 = EventBus.getDefault();
		System.out.println("Sagar>>> from single item>>>>>>>>>>" + bus2.isRegistered(this));
		if (bus2.isRegistered(this)) {
			// do nothing
		} else {
			bus2.register(this);
			System.out.println("Sagar>>> from single item>>>>>>>>>>" + bus2.isRegistered(this));
		}
	}

	@SuppressLint("NewApi")
	public void onEventMainThread(PassItem event) {
		// tv1.setText(event.s.toString());
		Log.d("Sagar", "before settext");
		Log.d("Sagar", event.s.toString());
		Log.d("Sagar", "after settext");
		String key1 = "language";
		String key2 = "flag_path";
		String key3 = "country";
		tv3.setText(event.s.get(key3).toString());
		System.out.println("title>>>>>>>>>>>" + event.s.get(key3).toString());
		tv1.setText(event.s.get(key1).toString());
		// tv2.setText( event.s.get(key2).toString());
 
		imageLocation = event.s.get(key2).toString();
		try {
			StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
					.permitAll().build();

			StrictMode.setThreadPolicy(policy);
			InputStream is = (InputStream) new URL(imageLocation).getContent();
			Drawable d = Drawable.createFromStream(is, "src name");
			imgv.setImageDrawable(d);

		} catch (Exception e) {
			Log.d("Sagar", "ERROR : " + e); 

		}
	}

}
