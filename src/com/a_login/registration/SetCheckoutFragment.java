package com.a_login.registration;

import globals.ProductsList;
import java.util.List;
import bean.Product;
import com.google.android.gms.wallet.MaskedWallet;
import com.google.android.gms.wallet.MaskedWalletRequest;
import com.google.android.gms.wallet.WalletConstants;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;
import android.os.Build;

public class SetCheckoutFragment extends IWantWalletFragment {

	private static final int REQUEST_CODE_USER_LOGIN_WALLET = 1006;
	private boolean mGoogleWalletDisabled = false;
	private List<Product> mCartList;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		mCartList = ProductsList.getInstance().getCart();
	}

	@Override
	public View onCreateView(
			LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

		initializeProgressDialog();

		View view = inflater.inflate(R.layout.fragment_set_checkout, container, false);
		buyWithGoogleWallet();
		return view;
	}

	private void buyWithGoogleWallet() {
		loadMaskedWallet();
	}

	private void loadMaskedWallet() {
		if (mWalletClient.isConnected()) {
			mProgressDialog.show();
			mWalletClient.loadMaskedWallet(createMaskedWalletRequest(),
					REQUEST_CODE_RESOLVE_LOAD_MASKED_WALLET);
		} else {
			if (!mWalletClient.isConnected() && !mWalletClient.isConnecting()) {
				mWalletClient.connect();
			}
			mHandleMaskedWalletWhenReady = true;
		}
	}

	private MaskedWalletRequest createMaskedWalletRequest() {
		return WalletUtil.createMaskedWalletRequest(mCartList.get(0));
	}

	@SuppressLint("NewApi")
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		switch (requestCode) {
		case REQUEST_CODE_RESOLVE_ERR:
			// call connect regardless of success or failure
			// if the result was success, the connect should succeed
			// if the result was not success, this should get a new connection result
			mWalletClient.connect();
			break;
		case REQUEST_CODE_RESOLVE_LOAD_MASKED_WALLET:
			if (mProgressDialog.isShowing()) {
				mProgressDialog.dismiss();
			}
			switch (resultCode) {
			case Activity.RESULT_OK:
				MaskedWallet maskedWallet =
				data.getParcelableExtra(WalletConstants.EXTRA_MASKED_WALLET);
				launchConfirmationPage(maskedWallet);
				break;
			case Activity.RESULT_CANCELED:
				// nothing to do here
				break;
			default:
				int errorCode = data.getIntExtra(WalletConstants.EXTRA_ERROR_CODE, 0);
				handleError(errorCode);
				break;
			}
			break;
		case REQUEST_CODE_USER_LOGIN_WALLET:
			// User successfully logged in, time to continue their checkout flow
			// If the user canceled out of the login screen don't do anything.
			if (resultCode == Activity.RESULT_OK) {
				// Recreating the menu so it now shows Logout
				getActivity().invalidateOptionsMenu();
				buyWithGoogleWallet();
			}
			break;
		default:
			break;
		}
	}

	@Override
	protected void handleError(int errorCode) {
		switch (errorCode) {
		case WalletConstants.ERROR_CODE_SPENDING_LIMIT_EXCEEDED:
			Toast.makeText(getActivity(),
					getString(R.string.spending_limit_exceeded, errorCode),
					Toast.LENGTH_LONG).show();
			break;
		case WalletConstants.ERROR_CODE_INVALID_PARAMETERS:
		case WalletConstants.ERROR_CODE_AUTHENTICATION_FAILURE:
		case WalletConstants.ERROR_CODE_BUYER_ACCOUNT_ERROR:
		case WalletConstants.ERROR_CODE_MERCHANT_ACCOUNT_ERROR:
		case WalletConstants.ERROR_CODE_SERVICE_UNAVAILABLE:
		case WalletConstants.ERROR_CODE_UNSUPPORTED_API_VERSION:
		case WalletConstants.ERROR_CODE_UNKNOWN:
		default:
			// unrecoverable error
			mGoogleWalletDisabled = true;
			//displayGoogleWalletErrorToast(errorCode);
			break;
		}
	}

	private void launchConfirmationPage(MaskedWallet maskedWallet) {
		System.out.println("launchConfirmationPage >>>>>>>>>>>");
		Intent intent = new Intent(getActivity(), ConfirmationActivity.class);
		intent.putExtra(Constants.EXTRA_ITEM_ID, mItemId);
		intent.putExtra(Constants.EXTRA_MASKED_WALLET, maskedWallet);
		startActivity(intent);
	}

	@Override
	public void onConnected(Bundle connectionHint) {
		if (mHandleMaskedWalletWhenReady) {
			loadMaskedWallet();
		}
	}

	private void displayGoogleWalletUnavailableToast() {
		Toast.makeText(getActivity(), R.string.google_wallet_unavailable, Toast.LENGTH_LONG).show();
	}


}
