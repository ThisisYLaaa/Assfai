# Tile Placement

When it comes to constructing your level, the editor allows you to input each tile using the keyboard. There are also several methods to custom input an angle into the game. Before we continue, here is how the image will be subtitled for your understanding:

* **White Letters** - Keyboard Shortcut for tile placement
* <mark style="color:yellow;">**Yellow Lines and Angles**</mark> - 90º Separation placement and their associated angles
* <mark style="color:blue;">**Blue Lines and Angles**</mark> - 45º Separation placement and their associated angles
* <mark style="color:green;">**Green Lines and Angles**</mark> - 30º Separation placement and their associated angles
* <mark style="color:red;">Red Lines and Angles</mark> - 15º Separation placement and their associated angles

Let's now learn how to start counting angles **according to the planet's rotation**. All examples will be based out of a `4/4` Tempo Signature, which is the most commonly used around most songs. Each angle will be counting from 0º at its most right side radius, turning counter-clockwise and increasing this number until one full lap around is complete, where it goes back to 0º

{% hint style="info" %}
Learning this angle measure is efficient as your level will register angles into your <mark style="color:orange;">Angle Data</mark> portion on your level files. Learn more about this on [Surgery](https://adofaieditor.gitbook.io/english/surgery) Page
{% endhint %}

## 90º Angles

Starting from the basics, 90º placements are the simplest to use, as they represent our on-beats and off-beats of the song

So let's consider that every time we hit 0º, we are doing 1 beat into the song beat

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FI8rQlPQXHu30Ea7Py8Xg%2FCompass%200%20degrees.png?alt=media&#x26;token=1f9557f7-ed8f-46cb-9629-c3943ec23ffe" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet where each sheet beat, equals the start of an angle (0º degrees)</p></figcaption></figure>

#### • Example 1

According to the game tile values, each tile represents an angle. Said angle is always base out of a counter-clockwise rotation from each beat, meaning 1 beat equals a starting point of an angle value.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FTSFX7nnuil72L9I0DBR2%2F2023-06-27%2016-32-27.mp4?alt=media&loop=false&token=710d9f7f-501f-43b4-9145-ad77d0be03af>" %}

With this in mind, every time you place a tile that isn't at beat start, its angle value will increase depending on how its angle ends, based from the beat start position.

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FpxzkM1K2zzRApGccGap6%2F90%20angles.png?alt=media&#x26;token=99dd1a03-904d-4449-bde3-7e4e9ee7a553" alt="" width="563"><figcaption><p>Angle Rotation - 90º Splits</p></figcaption></figure>

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2Fq1T5X1mcShMi5ejiU10P%2FCompass%200%20degrees%20with%20offbeats.png?alt=media&#x26;token=77a6404d-c384-4d4a-8719-e97f70f6e71d" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, now with off-beat indicators </p></figcaption></figure>

These vertical angles (90º and 270º) are what we call off-beats, meaning they can occur in between each beat

#### • Example 2

Notice how the last horizontal tile had an angle of 180º? This is due to the origin point of the track being left to right, meaning this angle has a value of half a circle = 180º

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FZS5eYdaYy7zUK2rSQlvo%2F2023-06-27%2016-40-05.mp4?alt=media&token=c34f1e05-5d6c-44e4-b6f3-d24e931ae348>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FcSMroFP8KqrX4mTA5a8q%2FCompass%2090%20degrees.png?alt=media&#x26;token=ca83b1ef-8f4d-4a19-95d2-a6df6dfeff25" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, using off-beats </p></figcaption></figure>

#### • Example 3

Same logic applies here, each angle doing down has to turn a radius angle from the right to left, so 1 and a half circle = 270º

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FXJIipV8tIlMEFF2WBXtP%2F2023-06-27%2016-46-10.mp4?alt=media&token=d0733d8b-b301-4eaa-add0-8036e3dc8cbd>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FcTYMTaY1p7SDyQpRDmhp%2FCompass%20270%20degrees.png?alt=media&#x26;token=75581d69-bb89-42b7-8817-2e415bdfbe85" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, using long off-beats </p></figcaption></figure>

#### • Example 4

This case is a bit tricky. Each angle, compared to the last one, is a 90º different, however, when counting angles always remember to do it counter-clockwise, always starting from the beat line radius angle.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FR3oxhtNHPttU5RfrsHmq%2F2023-06-27%2016-58-32.mp4?alt=media&token=dee11037-3314-43e1-89f7-944c27bf7173>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FmJ7an9aln6sS6qIPjKHP%2FCompass%20squares%20degrees.png?alt=media&#x26;token=7d0d9bc6-5e79-4ed9-9998-1851406c74d9" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, mixing on-beats and off-beats</p></figcaption></figure>

In conclusion, the angles presented in the square are 0º, 90º, 180º, 270º and 0º again. These are the angles the game file will record to make the square form.

## 45º Angles

Now that we got the hang of on-beats and off-beats, let's add one more beat in between those. We now can play 4 beats inside each sheet beat. Each beat now is considered a sixteenth note

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FBitE6ywsoU2EEpphnhdk%2FCompass%2045%20degrees%20with%20offbeats.png?alt=media&#x26;token=78b45098-7ce0-481c-a34f-1c077bb70d6d" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet with 4 splits of 45º each sheet beat</p></figcaption></figure>

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FxwheWY5SHGJQ8leAoXx6%2F45%20angles.png?alt=media&#x26;token=7c507961-754d-4f33-8829-97af5308cdf6" alt="" width="563"><figcaption><p>Angle Rotation - 45º Splits</p></figcaption></figure>

#### • Example 1

For this example, you can see that we created a tile that doesn't go fully horizontal, nor vertical. Sixteenths splitting allow notes to be played in between on-beats and off-beats

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F3DUobSir3G3CJFNL6ayV%2F2023-06-27%2017-15-52.mp4?alt=media&token=1b688e44-811e-41d1-8545-b348f5605a25>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FwpQp4CqfewRXAhguxzcB%2FCompass%2045%20degrees.png?alt=media&#x26;token=78cd602c-40ef-4764-82e2-d4d1fe143fbc" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, showing 45º angles</p></figcaption></figure>

#### • Example 2

This is how a curve using the previous sixteenths angles would look like. As the sum of some sixteenths angles is equal to some off-beat and on-beat notes, those tiles also appear in the sixteenth curve to support the rhythm

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FHDEY1j5Z2Svbkx169gUX%2FCompass%2045%20curve%20degrees.mp4?alt=media&token=dcd68b03-e2ad-41bf-81e8-32f028af3760>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FZir2QlirphupsPfZ7lLb%2FCompass%2045%20curve%20degrees.png?alt=media&#x26;token=db05791f-8505-473d-992e-677cf3d35484" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, curve tile using 45º angles</p></figcaption></figure>

#### • Example 3

Following the logic of a square pattern, we can build one using only intervals from the sixteenth placement, making all angles be hit in between on-beats and off-beats

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FcEGIPdl1zOKq4l9TyD2I%2FCompass%2045%20squares%20degrees.mp4?alt=media&token=11f03e40-1c2b-43f9-b6ac-5c3b18306202>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FFrzbENWWSJfU2NhDgu4P%2FCompass%2045-135%20squares%20degrees.png?alt=media&#x26;token=e1314dcf-e4f3-4cac-b1c1-b5e3f68bf9a7" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, making squares of sixteenth</p></figcaption></figure>

## 30º Angles

These angles are mostly used for swing style of music, but the tile placement logic is the same. Take in consideration the 45º angles, where we placed 1 beat in between each on-beat and off-beat. This time, we are placing two beats in between each, rather than one, allowing us to count 24 beats in each sheet compared to the 16 beats from the 45º angles.

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FmMTiV3WLMHZZyfPGfedo%2FCompass%2030%20degrees%20with%20offbeats.png?alt=media&#x26;token=344fb9d5-56d4-4728-a8e6-0aaf7252c276" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet with 6 splits of 30º each sheet beat</p></figcaption></figure>

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FU0y0mX0VoPlxHJI97Y25%2F30%20angles.png?alt=media&#x26;token=9b647b4e-f255-49bd-a84d-32f3c607aade" alt="" width="563"><figcaption><p>Angle Rotation - 30º Splits</p></figcaption></figure>

{% hint style="info" %}
You can access these shortcut tiles by holding <mark style="color:yellow;">`Shift`</mark> during the placement
{% endhint %}

#### • Example 1

Similar to 45º angle example, you can see that we created a tile that doesn't go fully horizontal, nor vertical, however since we have two beats between those angles, we can go beyond a perfect middle angle, but one that equally divided more to the horizontal angle, and another more to the vertical angle.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FJkEWhJM0g1KhKThCdxIA%2F2023-06-27%2018-01-51.mp4?alt=media&token=e60fe499-74a7-455e-8d41-d59d00956cd8>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FkPtbfNvgoCUX7hKn6A0l%2FCompass%2030%20degrees.png?alt=media&#x26;token=98cca718-eb7e-4869-abc0-a1f08fbad3f3" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, showing 30º angles</p></figcaption></figure>

#### • Example 2

A curve that fits the 4/4 tempo is only possible if we use angles above 90º, which means 30º angles will be taking too long, requiring more than one sheet of 4/4 tempo. So we are using what we call the Hexagons (Curves made out of 120º angles). For this example, you can see how a swing beat can interact with a full rotation angle tile.

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FyhRlwbiRmbaQvIHm51XG%2F2023-06-27%2018-11-43.mp4?alt=media&token=20a665aa-fb74-4788-82cf-cf7610c4ada6>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FH12Jzgmj5rJWyngtSae2%2FCompass%2060%20curve%20degrees.png?alt=media&#x26;token=ede74ac7-934e-4da8-9f80-389e6f792993" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, curve half hexagon using 60º angles</p></figcaption></figure>

#### • Example 3

Making squares on swing tempos can be a bit tricky. These come from a mix of on-beats and swings beats, to create the jazzy gameplay style.&#x20;

{% embed url="<https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FsvEuXVwuEYzeeDK0Hnjj%2F2023-06-27%2018-19-40.mp4?alt=media&token=1b009394-f5be-4a02-9e55-2da7f0f08d37>" %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F38CoeYMzFgsIiZNGM4sx%2FCompass%2060-240%20squares%20degrees.png?alt=media&#x26;token=41d4f63e-f841-4b50-aaaf-5de1bdb6f5fa" alt="" width="375"><figcaption><p>Tempo - 4/4 Sheet, making squares of 60º angles</p></figcaption></figure>

Take into consideration that we are using the same angles for both the on-beats used, but alternatives to these angles are possible too. So get creative and place some tiles around, get creating!

## 15º Angles

As an extra demonstration, the game allows you to fast input 15º Angles&#x20;

{% hint style="info" %}
You can access these shortcut tiles by holding <mark style="color:yellow;">`Shift`</mark>`+`` `<mark style="color:yellow;">`` ` ``</mark> during the placement
{% endhint %}

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FL6DwGdkdFqZcxegBxrom%2F15%20angles.png?alt=media&#x26;token=3a350103-9cc2-453a-8662-1c86db6f3807" alt="" width="563"><figcaption><p>Angle Rotation - 15º Splits</p></figcaption></figure>

## Custom Angles

If any of these methods won't do for your levels, you can customize the exact angle you're looking for. To insert a custom angle, press the angle button after selecting the tile you want to insert the angle from.

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2Ft9LsrB6D8qre5Vuw4Ha1%2Fimagem.png?alt=media&#x26;token=190aee42-1821-406e-a2a6-bdbadf05a5d6" alt="" width="375"><figcaption><p>Editor - Insert Angle Button</p></figcaption></figure>

From there, your options should look like the image below. Simply write your angle inside the text box, and click in one of the two tile types, to add the desired angle. (Regular tile or Mid-spin tile)

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FZLf5j9Dw75trsErUBugy%2Fimagem.png?alt=media&#x26;token=ac583c5d-38b3-4c17-a5b1-8f9decb092d8" alt="" width="299"><figcaption><p>Editor - Select type of tile and angle text box</p></figcaption></figure>

As you can see from the image below, one 15º angle tile was added to your track. This angle was the calculation from the last tile position angle + your angle value, creating a 165º angle that is a **difference of 15º angle**, between your last tile and the new one!

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FBj6OisGCcoSnIOME9chr%2Fimagem.png?alt=media&#x26;token=6f69f56b-9f7e-49d9-87d4-523b0021fab0" alt="" width="375"><figcaption><p>Editor - Inserted a tile with 15º Angle apart, based on the last tile angle. (165º on the editor file)</p></figcaption></figure>

{% hint style="warning" %}
These angle inputs always measure clockwise from the **last tile angle position**, rather than angle 0º as explained for your <mark style="color:orange;">Angle Data</mark> storage values. These inputs are merely informative to help place custom angles and their values are not stored based on them.
{% endhint %}

## Tile Placement Shortcuts

#### • 45º Angles

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2F35KoGOxenm7I8tVyVUvg%2Fimagem.png?alt=media&#x26;token=e557070d-51b9-44a9-b912-c175baa29d6c" alt="" width="308"><figcaption><p>Shortcuts for 45º Angles tiles</p></figcaption></figure>

#### • 30º Angles

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FqQisdRFebJ9B5Mj2qPQd%2Fimagem.png?alt=media&#x26;token=40633377-1ebf-45c2-97fb-bb735a4a951f" alt="" width="308"><figcaption><p>Shortcuts for 30º Angles tiles</p></figcaption></figure>

#### • **15º Angles**

<figure><img src="https://484108807-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fipb5NkFjq0eBOIGewqlQ%2Fuploads%2FlzfYh6KrQiXq2Au72r4P%2Fimagem.png?alt=media&#x26;token=ed9d8b1d-5e51-4024-adae-60f11e816b5e" alt="" width="310"><figcaption><p>Shortcuts for 15º Angles tiles</p></figcaption></figure>


---

