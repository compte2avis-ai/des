from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ⚙️ CONFIGURATION
TOKEN = "8736667685:AAGI5yXvHD5ZDB18on43wIjJQYI3cBzPQ9w"  # 👈 N'OUBLIE PAS DE METTRE TON TOKEN ICI !
ADMIN_ID = 8564548755    # ✅ Ton ID est configuré

# 💰 TES ADRESSES ET LIENS (Configurés)
WALLET_LTC = "ltc1qwy40a9gr0r3mz65vky2nx3zuq6txz7ffuxhxpn"
WALLET_ETH = "0x5900e982f8189F93b88A1290dB8Bc62F779D2b48"
PAYPAL_LINK = "https://paypal.me/AbdoulayeFofanah777"
TON_USERNAME = "@X4RCS"
CODE_PROMO = "X4RCS"

# --- 1. COMMANDE /START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = (
        "🌟 <b>Bienvenue sur Nextbox !</b> 🌟\n\n"
        "La boutique n°1 pour acheter tes étoiles Telegram au meilleur prix. 🚀\n"
        "Profite de nos offres exclusives et de nos paiements sécurisés.\n\n"
        f"📩 <b>Support :</b> {TON_USERNAME}\n\n"
        "👇 <i>Que souhaites-tu faire ?</i>"
    )
    keyboard = [
        [InlineKeyboardButton("⭐ Acheter des étoiles", callback_data="acheter")],
        [InlineKeyboardButton("🎟️ Code Promo", callback_data="promo")]
    ]
    await update.message.reply_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 2. CHOIX DU PACK ---
async def bouton_acheter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    texte = (
        "🛒 <b>Choisis ton pack d'étoiles</b> ⭐️\n\n"
        "Voici nos offres exclusives (paiement instantané) :"
    )
    keyboard = [
        [InlineKeyboardButton("⭐ 500 étoiles - 8,00€", callback_data="pack_500")],
        [InlineKeyboardButton("⭐ 1000 étoiles - 16,00€", callback_data="pack_1000")],
        [InlineKeyboardButton("⭐ 2500 étoiles - 40,00€", callback_data="pack_2500")],
        [InlineKeyboardButton("⭐ 5000 étoiles - 80,00€", callback_data="pack_5000")],
        [InlineKeyboardButton("⭐ 10000 étoiles - 150,00€", callback_data="pack_10000")],
        [InlineKeyboardButton("🔙 Retour", callback_data="start")]
    ]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 3. CHOIX DU MOYEN DE PAIEMENT ---
async def choix_paiement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pack = query.data.split('_')[1]
    context.user_data['pack'] = pack
    texte = (
        f"✅ <b>Pack sélectionné : {pack} étoiles ⭐️</b>\n\n"
        "💳 <b>Comment souhaites-tu payer ?</b>"
    )
    keyboard = [
        [InlineKeyboardButton("🅿️ PayPal", callback_data="pay_paypal")],
        [InlineKeyboardButton("🪙 Crypto", callback_data="pay_crypto")],
        [InlineKeyboardButton("🔙 Retour", callback_data="acheter")]
    ]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 4. CHOIX DE LA CRYPTO ---
async def choix_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    texte = (
        "🪙 <b>Quelle crypto souhaites-tu utiliser ?</b>\n\n"
        "Choisis ta devise :"
    )
    keyboard = [
        [InlineKeyboardButton("🔷 Ethereum (ETH)", callback_data="crypto_ETH")],
        [InlineKeyboardButton("🔵 Litecoin (LTC)", callback_data="crypto_LTC")],
        [InlineKeyboardButton("🔙 Retour", callback_data="acheter")]
    ]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 5. ENVOI DE LA COMMANDE À L'ADMIN ---
async def recevoir_commande(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "pay_paypal":
        moyen = "PayPal"
    else:
        moyen = data.split('_')[1]
    context.user_data['moyen'] = moyen
    client_id = query.message.chat.id
    client_nom = query.from_user.username or query.from_user.first_name
    pack = context.user_data.get('pack', 'Inconnu')
    
    texte_client = (
        "⏳ <b>Commande enregistrée !</b>\n\n"
        "Ta commande est en cours de traitement par un administrateur. "
        "Tu recevras les informations de paiement dans quelques instants. Patiente..."
    )
    await query.edit_message_text(texte_client, parse_mode="HTML")
    
    texte_admin = (
        f"🚨 <b>NOUVELLE COMMANDE</b> 🚨\n\n"
        f"👤 Client : @{client_nom} (ID: {client_id})\n"
        f"⭐️ Pack : {pack} étoiles\n"
        f"💳 Paiement : {moyen}\n\n"
        f"👇 Clique sur Confirmer pour envoyer les infos de paiement au client."
    )
    keyboard = [[InlineKeyboardButton("✅ Confirmer", callback_data=f"admin_confirm_{client_id}_{moyen}")]]
    await context.bot.send_message(chat_id=ADMIN_ID, text=texte_admin, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 6. ACTION DE L'ADMIN : CONFIRMER ---
async def admin_confirmer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split('_')
    client_id = int(parts[2])
    moyen = parts[3]
    
    if moyen == "PayPal":
        adresse = PAYPAL_LINK
        devise = "PayPal"
        instruction = "Clique sur ce lien pour effectuer le paiement :"
    elif moyen == "ETH":
        adresse = WALLET_ETH
        devise = "Ethereum (ETH)"
        instruction = "Envoie le montant exact à cette adresse :"
    else:
        adresse = WALLET_LTC
        devise = "Litecoin (LTC)"
        instruction = "Envoie le montant exact à cette adresse :"
        
    texte_client = (
        f"💸 <b>Voici les informations de paiement</b> 💸\n\n"
        f"Mode : <b>{devise}</b>\n"
        f"{instruction}\n"
        f"<code>{adresse}</code>\n\n"
        "👇 <i>Effectue le paiement puis attends la confirmation de l'administrateur.</i>"
    )
    await context.bot.send_message(chat_id=client_id, text=texte_client, parse_mode="HTML")
    
    texte_admin = (
        f"✅ Infos <b>{devise}</b> envoyées au client !\n\n"
        f"👇 Clique sur J'ai reçu quand le paiement est validé."
    )
    keyboard = [[InlineKeyboardButton("💰 J'ai reçu", callback_data=f"admin_recu_{client_id}")]]
    await query.edit_message_text(texte_admin, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 7. ACTION DE L'ADMIN : J'AI REÇU ---
async def admin_recu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    client_id = int(query.data.split('_')[2])
    
    texte_client = (
        "🎉 <b>Merci pour ton achat !</b> 🎉\n\n"
        "Ton paiement a bien été reçu. ✅\n"
        "Tes étoiles seront créditées sur ton compte Telegram d'ici <b>1 à 2 jours maximum</b>. ⭐️\n\n"
        "Merci de ta confiance et à très vite sur Nextbox ! 🚀"
    )
    await context.bot.send_message(chat_id=client_id, text=texte_client, parse_mode="HTML")
    await query.edit_message_text("✅ Commande terminée avec succès. Le client a été notifié.")

# --- 8. BOUTON CODE PROMO ---
async def bouton_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    texte = (
        "🎟️ <b>Code Promo</b> 🎟️\n\n"
        "Pour profiter de nos offres, utilise le code promo suivant :\n\n"
        f"👉 <code>{CODE_PROMO}</code> 👈\n\n"
        "⚠️ <i>Copie ce code et envoie-le en message à l'administrateur pour valider ta réduction !</i>"
    )
    keyboard = [[InlineKeyboardButton("🔙 Retour", callback_data="start")]]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 9. VÉRIFICATION DU CODE PROMO ---
async def verifier_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = update.message.text.strip().upper()
    if texte == CODE_PROMO:
        await update.message.reply_text(
            "✅ <b>Code promo validé !</b> 🎉\n\n"
            "Ta réduction a bien été prise en compte. Contacte l'administrateur pour finaliser ton achat.",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            "❌ <b>Code invalide.</b>\n\n"
            "Vérifie le code et réessaie.",
            parse_mode="HTML"
        )

# --- DÉMARRAGE DU BOT ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(bouton_acheter, pattern="^acheter$"))
    app.add_handler(CallbackQueryHandler(choix_paiement, pattern="^pack_"))
    app.add_handler(CallbackQueryHandler(choix_crypto, pattern="^pay_crypto$"))
    app.add_handler(CallbackQueryHandler(recevoir_commande, pattern="^pay_paypal$|^crypto_"))
    app.add_handler(CallbackQueryHandler(admin_confirmer, pattern="^admin_confirm_"))
    app.add_handler(CallbackQueryHandler(admin_recu, pattern="^admin_recu_"))
    app.add_handler(CallbackQueryHandler(bouton_promo, pattern="^promo$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verifier_code))
    
    print("Le bot Nextbox est en ligne !")
    app.run_polling()