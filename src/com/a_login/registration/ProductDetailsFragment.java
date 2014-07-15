package com.a_login.registration;



import java.util.List;

import bean.Product;
import globals.ProductsList;
import android.annotation.SuppressLint;
import android.app.Fragment;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

/**
 * A simple {@link android.support.v4.app.Fragment} subclass.
 * 
 */
@SuppressLint("NewApi")
public class ProductDetailsFragment extends Fragment {

	TextView tv1;
	TextView tv3;
	TextView price;
	ImageButton addToCart;
	ImageView imgv;
	ProductsList productsList;
	int position;
	public ProductDetailsFragment() {
		// Required empty public constructor
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		// Inflate the layout for this fragment
		position = getArguments().getInt("com.a_login.registration.ProductDetailsActivity.position");
		productsList = ProductsList.getInstance();
		return inflater
				.inflate(R.layout.fragment_product_details, container, false);
	}

	@Override
	public void onActivityCreated(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onActivityCreated(savedInstanceState);
		final List<Product> cart = productsList.getCart();
		tv1 = (TextView) getActivity().findViewById(R.id.textView10);
		tv3 = (TextView) getActivity().findViewById(R.id.textView30);
		price = (TextView) getActivity().findViewById(R.id.price);
		imgv = (ImageView) getActivity().findViewById(R.id.imageView_single); 	
		addToCart = (ImageButton) getActivity().findViewById(R.id.button_add_to_cart);
		
		final Product product = productsList.getProductAt(position);

		String title = product.getTitle();
		String prodPrice = "$"+String.valueOf(product.getPrice());
		String desc = product.getDescription();
		Bitmap bmp = product.getImage();

		System.out.println("SUD >>>>"+title+" >>> "+desc+" >>> "+bmp);
		tv1.setText(desc);
		tv3.setText(title);
		price.setText(prodPrice);
		imgv.setImageBitmap(bmp);


		Log.d("Sagar", "inside onact  created singlitem");

		addToCart.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				cart.add(product);
				getActivity().finish();	

			}
		});

		/*// Disable the add to cart button if the item is already in the cart
		if(cart.contains(product)) {
			addToCart.setEnabled(false);
			addToCart.setText("Item in Cart");
		}*/

	}
}
