# Hidden Twirls and On-beat rotation

{% hint style="info" %}
This practice is related to [Twirl](https://adofaieditor.gitbook.io/english/events/gameplay-events/twirl) Events
{% endhint %}

## • Hidden Twirls

Twirls, when placed on bad spots in a level, can cause the gameplay to be impossible to read, as it may be covered by the track itself, making it hard/impossible for the player to know what to do next.

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FItilZ9hJ1ezgXqoNZYIg%2FCaptura%20de%20tela%202023-06-29%20003600.png?alt=media&#x26;token=c721febf-9e0f-462a-ac84-1f9d21f45d13" alt="" width="349"><figcaption><p><em>Twirl hidden behind a 90° turn tile</em></p></figcaption></figure>

In cases like these, it's better to move the twirl somewhere it's visible, while not affecting the gameplay itself in any way. But if that's not possible *(In this case, for demonstration purposes)*, Position Track events can always be used in order to fix this issue.

<div><figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FEDYdo8bRAIkiwLR6J0lc%2FCaptura%20de%20tela%202023-06-29%20003724.png?alt=media&#x26;token=1d47a4e2-7342-4601-bc62-eb3da61601c9" alt="" width="375"><figcaption><p><em>Twirl moved to the next tile on the track</em></p></figcaption></figure> <figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FRMTIMzXkLZ8Fkgh4hu31%2FCaptura%20de%20tela%202023-06-29%20003636.png?alt=media&#x26;token=fede188c-f7d1-4911-a0f6-8faf8911d3f3" alt="" width="360"><figcaption><p><em>Position Track events making the twirl be visible without changing the tile it is at</em></p></figcaption></figure></div>

## • On-Beat Rotation

On-Beat Rotation is when the angle turns don't add up to 180° or 360°, which represents the On-Beat of the song, and because of that, the sum of the angles, becomes the On-Beat of the song, despite not being 180° or 360°.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FrEXk3aOtjUGiULuEIhpS%2F2023-06-28%2000-05-04.mp4?alt=media&token=d17156ca-a3a8-4173-88b9-f0ed03a978d1>" %}
*On-Beat Rotation Example*
{% endembed %}

In the first pattern, the angles add up to 360°, avoiding On-Beat Rotation. `90+45+45+90+90=360°`

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FIbT4RZAEkJRBua4piY3w%2FCaptura%20de%20tela%202023-06-28%20003024.png?alt=media&#x26;token=eff74b83-6c71-40ec-8e3e-651c20fdb06c" alt=""><figcaption><p><em>Calculation made to find the current rotation of the track after the first pattern</em></p></figcaption></figure>

In the second pattern, the angles add up to -90°, causing On-Beat Rotation. Each time a twirl is used, the current operation is reversed. For example, in the image below, a twirl is used at the 45° turn, thus `-45`, and is used again for the next 45° turn, thus `+45`. `90-45+45-90-90=-90°`

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F0nPdHaxiWA2gS1mFCo2y%2FCaptura%20de%20tela%202023-06-28%20214924.png?alt=media&#x26;token=205f19a9-26f8-4249-8734-6117bc95a7e9" alt=""><figcaption><p><em>Calculation made to find the current rotation of the track after the second pattern</em></p></figcaption></figure>

This can be used well if you know what you can with it, but **to avoid it, the easiest way would be to only use twirls when there's an angle distance of 90°, 180°, 270° and 360° from the starting angle**. Of course, On-Beat Rotation is not always guaranteed to happen when twirls are used on non-cardinal angles, but beware of where you place them, so it doesn't happen unintentionally.


---

