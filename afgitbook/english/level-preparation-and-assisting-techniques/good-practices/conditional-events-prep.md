# Conditional Events Prep

{% hint style="info" %}
This practice is related to [Set Conditional](https://adofaieditor.gitbook.io/english/events/event-modifiers/set-conditional-events) Events
{% endhint %}

Setting conditions for certain events to happen during the level, is a great to create diversified content for each gameplay input. Basically, we can indicate the game when and what to do in case something happens in the level according to the player's input.

Here is a good example of <mark style="color:orange;">Conditional Events</mark> happening in the background of this level:

{% embed url="<https://youtu.be/Hhp-aRjOHmE?t=256>" %}
:pencil:ADOFAI - XT-X Options, gameplay by Nichipe
{% endembed %}

## How to set the conditions, so events can work?

{% hint style="info" %}
*Check the <mark style="color:purple;">Event Modifiers</mark> -* [*Set Conditional Events*](https://adofaieditor.gitbook.io/english/events/event-modifiers/set-conditional-events) *to properly initiate the event*
{% endhint %}

Every event, which includes an <mark style="color:purple;">**Event tag**</mark> setting, is available to use on the Conditional Events. For starters, let's use <mark style="color:orange;">Set Text</mark> and <mark style="color:orange;">Move Decoration</mark> as example

Create a text using the <mark style="color:orange;">Decorations</mark> Tab, let's leave the text empty for now. Next, add a new decoration and use any image you would like. Before we move into the actual events, we properly tag each decoration with their unique name

<div><figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FzjrKyYq2vQcFLcFcfIOQ%2Fimagem.png?alt=media&#x26;token=f9459d96-e591-4340-889a-aa2628ad4f6f" alt="" width="258"><figcaption><p>Example - Text tag</p></figcaption></figure> <figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FyCTywB1mTCXQURNkfflR%2Fimagem.png?alt=media&#x26;token=c1f5ba94-ddb8-47ae-8b2b-f15310f244b7" alt="" width="255"><figcaption><p>Example - Image tag</p></figcaption></figure></div>

Now, for our events, let's set a losing message and a decor rotation when the players lose during the level. Don't forget to add the previous tags into your events, so they work. We are also adding the <mark style="color:purple;">Event tag</mark> to our tag, so the conditional event can find which events to use.

<div><figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FnrQW2RJlMPmrpdS1ej8Z%2Fimagem.png?alt=media&#x26;token=c6f0a32e-b54d-47c6-b67c-204d09a06935" alt="" width="207"><figcaption><p>Example - Move Decoration prep for conditional event</p></figcaption></figure> <figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F6V8Sk0ejBxDusE5NVlDc%2Fimagem.png?alt=media&#x26;token=19a54f67-3fa1-4ba2-8e0d-bfeb6bf678c0" alt="" width="214"><figcaption><p>Example - Set Text prep for conditional event</p></figcaption></figure></div>

{% hint style="warning" %}
Make sure, when using tags for <mark style="color:orange;">Conditional Events</mark>, to use the **same event tag** on all your desired events, as each condition only accepts one tag.

Events will only work for <mark style="color:orange;">Conditional Events</mark> if they are built on the same tile as the conditional event
{% endhint %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FVRs174SuJuKwlhrptv4j%2Fimagem.png?alt=media&#x26;token=cb907af7-da33-4810-8a3c-49d1b31e9f52" alt=""><figcaption><p>Example - Event tag used for all "Loss" Events</p></figcaption></figure>

All it's needed now is to add the same event tag, into the "Loss" condition tag, since we only want these events to activate when the player loses. Rest assured, these events won't play in normal conditions when everything is set for conditional purposes.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FJAPc8FaeEyuJGBzEYYGX%2FSet%20Conditionals%20Prep.mp4?alt=media&token=bb351957-859d-47bc-98a3-dcc2b380854f>" %}

## Multiple Conditions set at the same time

Several events can be used for several conditions set at the same time, independently of what type they are. Let's use as an example several texts showing when the player input drifts from perfect using only one text decor.

<div><figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FMZZCCFPe14Cu6naAeTpt%2Fimagem.png?alt=media&#x26;token=bc766144-cbd9-458c-94de-2e478d78a30b" alt="" width="283"><figcaption><p>Example 2 - Setting a text for when the input is <br>Too Early / Too Late with a unique event tag</p></figcaption></figure> <figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F0IMHYY3HjLSwrJfyLg1l%2Fimagem.png?alt=media&#x26;token=46481066-da48-4ebf-8d69-15c573a61f91" alt="" width="273"><figcaption><p>Example 2 - Setting a text for when the input is <br>EPerfect/LPerfect with a unique event tag</p></figcaption></figure></div>

<div><figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2Fspe6ei4QFJABIt7MAouR%2Fimagem.png?alt=media&#x26;token=74fadea3-4644-4e76-85b2-788ab654649b" alt="" width="273"><figcaption><p>Example 2 - Setting a text for when the input is <br>Early/Late with a unique event tag</p></figcaption></figure> <figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2Febtik3qAgC2XOCD878vr%2Fimagem.png?alt=media&#x26;token=4d465aef-ad98-4ea7-b622-72d1df704970" alt="" width="275"><figcaption><p>Example 2 - Setting a text for when the input is <br>Perfect with a unique event tag</p></figcaption></figure></div>

For this example, we don't want any conditions for when the player loses, so we don't need to do any changes. For now, let's fill up the event tags in their respective places.

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FTmQRMbcNSNeeIPEMeuSx%2Fimagem.png?alt=media&#x26;token=d91b400f-0393-4563-9fcd-55f13518a23f" alt="" width="204"><figcaption><p>Example 2 - Setting each event tag on their respective condition</p></figcaption></figure>

Everything should work properly now. All the event tags were placed, and all events were set and connected to their conditions!

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FLaV6qrrZorMHCuHZmHwF%2F2023-06-29%2012-40-23.mp4?alt=media&token=7d4a5092-4142-4f35-a686-34aeb103af2f>" %}


---

