import React, { useEffect } from 'react';
import '../styles/GoogleTranslate.css';

const GoogleTranslate = React.memo(({ buttonText = "🌐 Lang" }) => {
    // Note: We removed state `isScriptLoaded` to prevent re-renders which wipe the DOM

    useEffect(() => {
        let intervalId = null;
        let timeoutId = null;

        const initGoogleTranslate = () => {
            // Check if already initialized to prevent double-injection if this effect runs twice
            const container = document.getElementById('google_translate_element');
            if (container && container.hasChildNodes()) {
                // Already has content, just update text
                updateButtonText();
                return;
            }

            try {
                if (window.google && window.google.translate && window.google.translate.TranslateElement) {
                    new window.google.translate.TranslateElement({
                        pageLanguage: 'en',
                        includedLanguages: 'en,hi,bn,te,mr,ta,ur,gu,kn,ml,pa',
                        layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
                        autoDisplay: false
                    }, 'google_translate_element');

                    // Wait for the Google Translate widget to be ready and style it
                    timeoutId = setTimeout(() => {
                        updateButtonText();
                    }, 500);
                }
            } catch (e) {
                console.error("Error initializing Google Translate:", e);
            }
        };

        const updateButtonText = () => {
            const translateButton = document.querySelector('.goog-te-gadget-simple span');
            if (translateButton) {
                translateButton.textContent = buttonText;
            }
            const accessibilityDiv = document.querySelector('.goog-te-gadget-simple .VIpgJd-ZVi9od-ORHb-OEVmcd');
            if (accessibilityDiv) {
                accessibilityDiv.setAttribute('aria-label', buttonText);
            }
        };

        window.googleTranslateElementInit = initGoogleTranslate;

        // Check if script is already present
        const existingScript = document.getElementById('google-translate-script');

        if (!existingScript) {
            const script = document.createElement('script');
            script.id = 'google-translate-script';
            script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
            script.async = true;
            script.onerror = () => console.error('Failed to load Google Translate script');
            document.body.appendChild(script);
        } else {
            // Script exists, check if loaded
            if (window.google && window.google.translate) {
                initGoogleTranslate();
            } else {
                // Poll for availability
                intervalId = setInterval(() => {
                    if (window.google && window.google.translate) {
                        initGoogleTranslate();
                        clearInterval(intervalId);
                    }
                }, 500);
            }
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

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Cleanup
        return () => {
            if (intervalId) clearInterval(intervalId);
            if (timeoutId) clearTimeout(timeoutId);
            observer.disconnect();
        };
    }, [buttonText]);

    return (
        <div
            id="google_translate_element"
            className="google-translate-container"
            style={{ minHeight: '40px', minWidth: '80px', display: 'inline-block' }}
        ></div>
    );
});

export default GoogleTranslate;