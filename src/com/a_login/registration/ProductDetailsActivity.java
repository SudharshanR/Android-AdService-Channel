package com.a_login.registration;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.FragmentTransaction;
import android.content.Intent;
import android.os.Bundle;

public class ProductDetailsActivity extends Activity {

	@SuppressLint("NewApi")
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_product_details);
		
		/*Intent intent = getIntent();
		ImageDetails imgDetails = (ImageDetails) intent.getParcelableExtra("img_details");
		*/
		

		//Bundle bundle = this.getIntent().getBundleExtra("bundle");
		Bundle bundle = new Bundle();
		int position = this.getIntent().getIntExtra("com.a_login.registration.IwantActivity.position", 0);
		bundle.putInt("com.a_login.registration.ProductDetailsActivity.position", position);
		ProductDetailsFragment details = new ProductDetailsFragment();
		details.setArguments(bundle);
		
		
		FragmentTransaction transaction = getFragmentManager().beginTransaction();
		//transaction.replace(R.id.productsList, singleItem);
		transaction.add(R.id.productdetails, details);
		//transaction.add(R.id.iwant_pager,singleItem);
        transaction.addToBackStack(null);

        // Commit the transaction
        transaction.commit();
	}

}
