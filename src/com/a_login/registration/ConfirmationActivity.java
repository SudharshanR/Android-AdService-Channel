package com.a_login.registration;

import android.content.Intent;
import android.os.Bundle;

/**
 * Activity that displays the user's Google Wallet checkout confirmation page.
 *
 * @see ConfirmationFragment
 */
public class ConfirmationActivity extends IWantWalletFragmentActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_confirmation);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        ConfirmationFragment fragment =
                (ConfirmationFragment) getSupportFragmentManager().findFragmentById(R.id.frag);
        fragment.onNewIntent(intent);
    }
}
