package com.a_login.registration;




import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;

import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;
import android.widget.ViewFlipper;

public class MainActivity extends Activity implements OnClickListener {
Button b,iwant;
ImageView imageview_iwant, imageview_deals, imageview_notifications, imageview_login, imageview_cart,  imageview_dealsnearme, imageview_logout;
int[] image ={R.drawable.smart_tv,R.drawable.smart_tv_2,R.drawable.smart_tv_3,R.drawable.smart_tv_4,R.drawable.smart_tv_5,R.drawable.smart_tv_6};
private ViewFlipper myViewFlipper;
SessionManager session;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		//session class instance created
		ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(getApplicationContext()).build();
		ImageLoader.getInstance().init(config);
		session = new SessionManager(getApplicationContext());
		//user log in status 
		imageview_logout = (ImageView) findViewById(R.id.imageView_home_logout);
		imageview_login = (ImageView) findViewById(R.id.imageView_home_login);

		if(session.isLoggedIn()){
			Toast.makeText(getApplicationContext(), "Welcome " + session.getUserName(), Toast.LENGTH_SHORT).show();
			imageview_login.setVisibility(View.INVISIBLE);
			imageview_logout.setVisibility(View.VISIBLE);
		}
		else
		{
			imageview_login.setImageResource(R.drawable.login3);
		}
		myViewFlipper = (ViewFlipper) findViewById(R.id.myflipper);

	    for (int i = 0; i < image.length; i++)
	    {
	        ImageView imageView = new ImageView(MainActivity.this);
	        imageView.setImageResource(image[i]);
	        myViewFlipper.addView(imageView);
	        myViewFlipper.setAutoStart(true);
	        myViewFlipper.setFlipInterval(3000);
	        myViewFlipper.startFlipping();
	        
	    }
		
		b = (Button) findViewById(R.id.button_loginmain);
		b.setOnClickListener(this);
		iwant = (Button) findViewById(R.id.button_iwant);
		iwant.setOnClickListener(this);
		imageview_iwant = (ImageView) findViewById(R.id.imageV_home_iwant);
		imageview_deals = (ImageView) findViewById(R.id.imageView_home_deals);
		imageview_notifications = (ImageView) findViewById(R.id.imageView_home_notification);
		imageview_cart = (ImageView) findViewById(R.id.imageView_home_shoppingcart);
		imageview_dealsnearme = (ImageView) findViewById(R.id.imageView_dealsnearme);
		imageview_iwant.setOnClickListener(this);
		imageview_login.setOnClickListener(this);
		imageview_deals.setOnClickListener(this);
		imageview_notifications.setOnClickListener(this);
		imageview_cart.setOnClickListener(this);
		imageview_dealsnearme.setOnClickListener(this);
		imageview_logout.setOnClickListener(this);
	}
	
	

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		if(v == b){
		Intent myIntent = new Intent(MainActivity.this, LoginActivity.class);
		startActivity(myIntent);
		}
		if(v == imageview_login){
			Intent myIntent2 = new Intent(MainActivity.this, LoginActivity.class);
			startActivity(myIntent2);
			}
		if(v== iwant){
			//switch to iwant activity
			Intent myIntent3 = new Intent(MainActivity.this, IwantActivity.class);
			startActivity(myIntent3);
			
		}
		if(v== imageview_iwant){
			//switch to iwant activity
			Intent myIntent4 = new Intent(MainActivity.this, IwantActivity.class);
			startActivity(myIntent4);
			
		}
		if(v== imageview_cart){
		    Intent viewShoppingCartIntent = new Intent(getBaseContext(), ShoppingCartActivity.class);
		    startActivity(viewShoppingCartIntent);			
		}
		
		if(v== imageview_notifications){
			//switch to iwant activity
			Intent myIntent7 = new Intent(MainActivity.this, Notification.class);
			startActivity(myIntent7);
			
		}
		if(v== imageview_deals){
			//switch to iwant activity
			Intent myIntent7 = new Intent(MainActivity.this, Deals_Activity.class);
			startActivity(myIntent7);
			
		}
		if(v== imageview_dealsnearme){
			//switch to deals near me activity
			Intent myIntent8 = new Intent(MainActivity.this, DealsNearMe.class);
			startActivity(myIntent8);
			
		}
		
		if(v== imageview_logout){
			//switch to deals near me activity
			imageview_logout.setVisibility(View.INVISIBLE);
			imageview_login.setVisibility(View.VISIBLE);
			session.logoutUser();

		}
	}

}
