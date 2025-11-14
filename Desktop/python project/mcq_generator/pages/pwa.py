"""
PWA Service Worker and Manifest injection
This file adds PWA capabilities to the Streamlit app
"""
import streamlit as st

def inject_pwa():
    """Inject PWA manifest and service worker"""
    st.markdown("""
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1f77b4">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="MCQ Generator">
    <link rel="apple-touch-icon" href="/icon-192.png">
    """, unsafe_allow_html=True)
    
    # Service Worker Registration
    st.markdown("""
    <script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/service-worker.js')
                .then(function(registration) {
                    console.log('ServiceWorker registration successful');
                }, function(err) {
                    console.log('ServiceWorker registration failed: ', err);
                });
        });
    }
    </script>
    """, unsafe_allow_html=True)

