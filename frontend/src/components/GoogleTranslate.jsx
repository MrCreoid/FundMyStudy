import React, { useEffect, useState } from 'react';
import '../styles/GoogleTranslate.css';

const GoogleTranslate = ({ buttonText = "🌐 Lang" }) => {
    const [isScriptLoaded, setIsScriptLoaded] = useState(false);

    useEffect(() => {
        const initGoogleTranslate = () => {
            if (window.google && window.google.translate && window.google.translate.TranslateElement) {
                const googleTranslateElement = new window.google.translate.TranslateElement({
                    pageLanguage: 'en',
                    includedLanguages: 'en,hi,bn,te,mr,ta,ur,gu,kn,ml,pa',
                    layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
                    autoDisplay: false
                }, 'google_translate_element');

                // Wait for the Google Translate widget to be ready
                setTimeout(() => {
                    const translateButton = document.querySelector('.goog-te-gadget-simple span');
                    if (translateButton) {
                        translateButton.textContent = buttonText;
                    }

                    // Also update the accessibility text
                    const accessibilityDiv = document.querySelector('.goog-te-gadget-simple .VIpgJd-ZVi9od-ORHb-OEVmcd');
                    if (accessibilityDiv) {
                        accessibilityDiv.setAttribute('aria-label', buttonText);
                    }

                    setIsScriptLoaded(true);
                }, 100);
            }
        };

        window.googleTranslateElementInit = initGoogleTranslate;

        // Load the Google Translate script if not already present
        if (!document.getElementById('google-translate-script')) {
            const script = document.createElement('script');
            script.id = 'google-translate-script';
            script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
            script.async = true;

            script.onload = () => {
                console.log('Google Translate script loaded');
            };

            script.onerror = () => {
                console.error('Failed to load Google Translate script');
            };

            document.body.appendChild(script);
        } else if (window.google && window.google.translate) {
            initGoogleTranslate();
        }

        // Mutation observer to handle dynamic changes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    const translateButton = document.querySelector('.goog-te-gadget-simple span');
                    if (translateButton && translateButton.textContent !== buttonText) {
                        translateButton.textContent = buttonText;
                    }
                }
            });
        });

        // Start observing
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Cleanup
        return () => {
            observer.disconnect();
        };
    }, [buttonText]);

    // Effect to update button text when buttonText prop changes
    useEffect(() => {
        if (isScriptLoaded) {
            const translateButton = document.querySelector('.goog-te-gadget-simple span');
            if (translateButton) {
                translateButton.textContent = buttonText;
            }
        }
    }, [buttonText, isScriptLoaded]);

    return (
        <div id="google_translate_element" className="google-translate-container"></div>
    );
};

export default GoogleTranslate;