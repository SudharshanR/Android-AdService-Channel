package com.a_login.registration;

import android.os.Bundle;

/**
 * Payment entry page.
 *
 * @see PaymentFragment
 */
public class PaymentActivity extends IWantWalletFragmentActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_payment);
    }
}
