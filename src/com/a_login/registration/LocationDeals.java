package com.a_login.registration;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;

public class LocationDeals extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_location_deals);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.location_deals, menu);
		return true;
	}

}
