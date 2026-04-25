# Smooth Pauses

{% hint style="info" %}
This practice is related to [Pause Tiles](https://adofaieditor.gitbook.io/english/events/gameplay-events/pause-tiles) Events
{% endhint %}

## • Pause indicators

Regarding pauses, these events are **not visible** to the player. So it is important to find creative ways to let the player know the pause tile exists, regardless of how long the pause is

#### **Using Gaps**

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FZS17OWtFB5smvBCaeWBq%2Fimagem.png?alt=media&#x26;token=e5bc30d0-6563-4b34-bc66-e2ede5fac49b" alt="" width="375"><figcaption><p>Pause - Using gaps and tile movement</p></figcaption></figure>

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FKva2SaPbuBLkFZB27HlD%2F2023-06-25%2012-39-19.mp4?alt=media&token=b1a4f379-73af-4512-a67d-ad7fc3f79d1f>" %}

#### **Using Colors**

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FRnA29I2Ac2e2foWTp4VR%2Fimagem.png?alt=media&#x26;token=57e0376c-4991-4656-8d5d-f6001ecb6eff" alt="" width="375"><figcaption><p>Pause - Color and Tile Format</p></figcaption></figure>

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FLqI7rNPfbpBRsGOSDXDi%2F2023-06-25%2012-45-15.mp4?alt=media&token=62f5d6ba-4e1b-435b-82c3-557e9853436f>" %}

## • Pause consistency

When it comes to using pauses, you have to take into consideration, these events are <mark style="color:red;">**not meant**</mark> to correct any offsets or adjust tile placement. So for this example, here's something you **shouldn't do**

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2Fjb7HU77sNa50ykGPPGr3%2F2023-06-25%2018-11-53.mp4?alt=media&token=dfdfe3a2-02fb-4292-bcd9-f8edf67ed8bb>" %}
Pause - Bad usage of pause tiles
{% endembed %}

To guarantee consistency, always use values that assure the beat doesn't create on-beat rotations. This is true for every angle the pause event is being active, 1 pause beat is always 180º no matter the tile angle:

180º -> 1 Pause Beat\
90º -> 0.5 Beats\
270º -> 1.5 Beats\
360º -> 2 Beats

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FS9EIShuGjvPOyE8T6qUO%2Fimagem.png?alt=media&#x26;token=69401deb-ffe0-4800-8700-c1b2c3847d4f" alt="" width="375"><figcaption><p>Pause - Rotation with angles</p></figcaption></figure>

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FnmPiGyrawRpIlBvT0QmY%2F2023-06-25%2018-31-02.mp4?alt=media&token=d168446d-dae6-4c2e-a013-e1e883253540>" %}


---

