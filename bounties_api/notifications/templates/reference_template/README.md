# What is this folder?

This folder contains 2 primary files. A `baseTemplate.html` file and an `index.css` file. Both of these files are used to create the base template for the Bounties Network Explorer email notifications.

## Instructions

The markup and styles for the template are separated in the reference folder to make it easier to edit the styles when changing the design of the base template.

_**Production templates should not use separate `.html` and `.css` files!**_

If you want to duplicate or copy from the reference template, and then want to propagate those changes across the production templates, you must use a [CSS inliner](https://putsmail.com/inliner) to inline all CSS before using the resulting `html` in your production template. _**If you do not first inline all styles, it will likely result in inconsistencies across email clients.**_

### Production Template Construction

`baseTemplate.html` should include most if not all of the elements that you need to construct a variety of notification variations. You may choose to omit elements as required by a particular notification. If you choose to do so, it is wise to also remove the `css` associated with the removed markup so that there is no unused `css`.

### Testing and Email Client Compatibility

The primary trouble-maker when it comes to `html` emails is Microsoft Outlook (often specifically for Windows). Whenever significant changes are made to email templates, it is wise to use a tool like [Litmus](https://litmus.com) to perform testing to ensure that the templates appear consistent across clients. It is best to use `<table>` for most elements in your markup in order to support as many clients as possible, especially Outlook.

Common culprits that can result in inconsistencies in Outlook include:

- Using `<div>` instead of `<table>`
- `@media` declarations (Media queries)
- CSS `display` and `position` properties
- `width` and `max-width` properties
- `border-radius`
- `padding` and `margin` applied to any elements other than `<td>` elements within tables.
- `img` elements with ill-defined size properties

In some cases, you may use conditional comments to add classes or target specific elements that need to be treated differently when being displayed in Outlook. The base template uses conditional commenting in several instances to display or hide certain content depending on the email client context. For the most part, these should remain unaltered.

#### Unless you intend to alter the design of the base template, please leave the base template unchanged, and only use it as a reference or to duplicate to create new production notification emails. Take care not to commit changed to `baseTemplate.html` and `index.css` unless that is your intent.
