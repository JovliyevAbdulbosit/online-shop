

from django.shortcuts import render
from telegram import Update , KeyboardButton, ReplyKeyboardMarkup , InlineKeyboardButton , InlineKeyboardMarkup
# Create your views here.
from .models import CategoryModel ,ProductModel ,KorzinkaModel
from django.core.paginator import Paginator



def start(update , context):
	user_id=update.message.from_user.id
	ctg=CategoryModel.objects.all()
	s=[]
	for i in ctg:
		btn=[InlineKeyboardButton(f'➡️{i.name}⬅️' , callback_data=f'{i.id}_{user_id}_1')]
		s.append(btn)
	s.append([InlineKeyboardButton("🛒Savatchani ko'rish" , callback_data=f'k_{user_id}_1')])	
	ctgbtn=	InlineKeyboardMarkup(s)
	update.message.reply_html("<b>Assalomu alaykum bizning Smartshop online do'konimizga xush kelibsiz</b>",
		reply_markup=ctgbtn)





	
def for_inline(update ,context):
	user_id=update.callback_query.from_user.id
	data_s=update.callback_query.data
	data_s=data_s.split('_')
	item=1
	if user_id==int(data_s[1]) and data_s[2]!='kor' and data_s[0] != 'k' and data_s[2]!='orqaga':
		product=ProductModel.objects.filter(ctg_id=data_s[0]).all()
		paginator = Paginator(product, 1)
		page_number=int(data_s[2])
		page_obj = paginator.get_page(page_number)
		
		if page_obj.has_previous() and page_obj.has_next():
			nexts=[[InlineKeyboardButton('⬅️orqaga' , callback_data=f'{data_s[0]}_{data_s[1]}_{page_obj.previous_page_number()}'),
			InlineKeyboardButton('oldinga➡️' , callback_data=f'{data_s[0]}_{data_s[1]}_{page_obj.next_page_number()}')],
			[InlineKeyboardButton("🛒savatga qo'shish" , callback_data=f'{data_s[0]}_{data_s[1]}_kor_{page_obj[0].id}'),
			InlineKeyboardButton("🏠home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]]
		elif page_obj.has_previous() :
		 	nexts=[[InlineKeyboardButton('⬅️orqaga' , callback_data=f'{data_s[0]}_{data_s[1]}_{page_obj.previous_page_number()}')],
		 	[InlineKeyboardButton("🛒savatga qo'shish" , callback_data=f'{data_s[0]}_{data_s[1]}_kor_{page_obj[0].id}'),
		 	InlineKeyboardButton("🏠home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]]
		elif page_obj.has_next() :
			nexts=[[InlineKeyboardButton('oldinga➡️' , callback_data=f'{data_s[0]}_{data_s[1]}_{page_obj.next_page_number()}')],
			[InlineKeyboardButton("🛒savatga qo'shish" , callback_data=f'{data_s[0]}_{data_s[1]}_kor_{page_obj[0].id}'),
			InlineKeyboardButton("🏠home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]]

		update.callback_query.message.reply_photo(caption=f"{page_obj[0].title}\n{page_obj[0].text}\n{page_obj[0].price}-so'm ",
			photo=open(f'media/{page_obj[0].rasm}', 'rb'),
			 reply_markup=InlineKeyboardMarkup(nexts))
		
	elif user_id==int(data_s[1]) and data_s[2]=='kor' and data_s[-1]!='savat' :
		product=ProductModel.objects.get(id=data_s[3])
		if len(data_s)>4:
			if data_s[4]=='-' :
				if int(data_s[5]) != 1:
					item=int(data_s[5]) -1
				elif int(data_s[5]) == 1:
					item=1

			elif data_s[4]=='+':
				item=int(data_s[5]) +1	
			soni=[[InlineKeyboardButton('-',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_-_{item}"),
			InlineKeyboardButton(f'{item}',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_{item}"),
			InlineKeyboardButton('+',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_+_{item}")],
			[InlineKeyboardButton("🛒Savatga qo'shish",callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_{item}_savat"),
			InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]]

			update.callback_query.message.edit_text('Sonini kiriting', reply_markup=InlineKeyboardMarkup(soni))	

		else:
			soni=[[InlineKeyboardButton('-',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_-_{item}"),
			InlineKeyboardButton(f'{item}',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_{item}"),
			InlineKeyboardButton('+',callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_+_{item}")],
			[InlineKeyboardButton("🛒Savatga qo'shish",callback_data=f"{data_s[0]}_{data_s[1]}_{data_s[2]}_{data_s[3]}_{item}_savat"),
			InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]]

			update.callback_query.message.reply_text('Sonini kiriting', reply_markup=InlineKeyboardMarkup(soni))
		
	elif user_id==int(data_s[1]) and data_s[-1]=='savat':
		pro=ProductModel.objects.get(id=int(data_s[3]))
		pay_p=KorzinkaModel()
		pay_p.haridor=data_s[1]
		
		pay_p.product=pro.title
		pay_p.soni=int(data_s[4])
		pay_p.total=int(data_s[4])*pro.price
		pay_p.save()
		ctg=CategoryModel.objects.all()
		s=[]
		for i in ctg:
			btn=[InlineKeyboardButton(f'➡️{i.name}⬅️' , callback_data=f'{i.id}_{user_id}_1')]
			s.append(btn)
		s.append([InlineKeyboardButton("🛒Savatni ko'rish " ,callback_data=f'k_{user_id}_1')])		
		ctgbtn=	InlineKeyboardMarkup(s)
		update.callback_query.message.edit_text("Savatga qo'shildi✅.\nKatigorya tanlang.\nagar tanlab bo'lgan bo'lsangiz savatga o'tib tasdiqlang",
			reply_markup=ctgbtn)
	elif data_s[2]=='orqaga':

		ctg=CategoryModel.objects.all()
		s=[]
		for i in ctg:
			btn=[InlineKeyboardButton(f'➡️{i.name}⬅️' , callback_data=f'{i.id}_{user_id}_1')]
			s.append(btn)
		s.append([InlineKeyboardButton("🛒Savatchani ko'rish" , callback_data=f'k_{user_id}_1')])		
		ctgbtn=	InlineKeyboardMarkup(s)
		update.callback_query.message.reply_text("Katigorya tanlang.\nagar tanlab bo'lgan bo'lsangiz savatga o'tib tasdiqlang",
			reply_markup=ctgbtn)
	elif data_s[0]=='k':
		kor_p=KorzinkaModel.objects.filter(haridor=int(data_s[1]))
		if not kor_p:
			ctg=CategoryModel.objects.all()
			s=[]
			for i in ctg:
				btn=[InlineKeyboardButton(f'{i.name}' , callback_data=f'{i.id}_{user_id}_1')]
				s.append(btn)
				
			ctgbtn=	InlineKeyboardMarkup(s)
			update.callback_query.message.edit_text("Sizning savatchangizda hech narsa yo'q. Kategorya tanlab mahsulot qo'shishingiz mumkin",
				reply_markup=ctgbtn)
		elif kor_p:

			if data_s[-1]=='delete':
				dele=KorzinkaModel.objects.get(id=int(data_s[2]))
				dels=dele.product
				dele.delete()
				kor_p=KorzinkaModel.objects.filter(haridor=int(data_s[1]))
				d=[]
				p=1
				for i in kor_p:
					if not i.is_deliver:
						sp=(i.product).split(' ')
						dp=sp[0]+' '+sp[1]+' '+sp[2]
						btns=[InlineKeyboardButton(f"{p}.{dp} ❌ soni {i.soni} ta ",callback_data=f"k_{user_id}_{i.id}_delete")]
						d.append(btns)
						p+=1
				if not kor_p :
					d.append([InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')])
				else:	
					d.append([InlineKeyboardButton("📝Tasdiqlash" , callback_data=f"k_{user_id}_tasdiqlash"),
						InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')])
				update.callback_query.message.edit_text(f"{dels} O'chirildi\n Tasdiqlash yoki o'chirishni tanlashingiz mumkin",
					reply_markup=InlineKeyboardMarkup(d))
			elif data_s[-1]=='tasdiqlash':
				context.bot.delete_message(message_id=update.callback_query.message.message_id,chat_id=update.callback_query.message.chat_id)
				context.bot.send_message(text="📞Telefon nomeringizni kiriti (masalan 906757449) yoki telefon nomer jo'natish tugmasini bosing",
                	chat_id=update.callback_query.message.chat_id , reply_markup=ReplyKeyboardMarkup([[KeyboardButton("📞Telefon nomer jo'natish" ,
                		request_contact=True )]], resize_keyboard=True))

			else:
				d=[]
				p=1
				for i in kor_p:
					if not i.is_deliver	:
						sp=(i.product).split(' ')
						dp=sp[0]+' '+sp[1]+' '+sp[2]
						btns=[InlineKeyboardButton(f"{p}.{dp} ❌ soni {i.soni} ta ",callback_data=f"k_{user_id}_{i.id}_delete")]
						d.append(btns)
						p+=1
				if d:		
					d.append([InlineKeyboardButton("📝Tasdiqlash" , callback_data=f"k_{user_id}_tasdiqlash"),
						InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')])
					update.callback_query.message.edit_text("Tasdiqlash yoki o'chirishni tanlashingiz mumkin",
						reply_markup=InlineKeyboardMarkup(d))
				else:
					d.append([InlineKeyboardButton("🏠Home" , callback_data=f'{data_s[0]}_{data_s[1]}_orqaga')]) 

					update.callback_query.message.edit_text("Sizning savatingizda hech narsa yo'q🤷‍♂️",
						reply_markup=InlineKeyboardMarkup(d))			
def contact(update,context):
	user_id=update.message.from_user.id
	user_name=update.message.from_user.username
	phone=update.message.contact.phone_number
	lists=KorzinkaModel.objects.filter(haridor=user_id)
	for i in lists:
		i.telefon=phone
		i.user_p=user_name
		i.save()


	update.message.reply_html("<b>Joylashuvni yuboring</b>" , reply_markup=ReplyKeyboardMarkup([[KeyboardButton('🗺Joylashuvni yuborish',
		request_location=True)]],resize_keyboard=True))		
def locations(update , context):
	a=update.message.location
	user_id=update.message.from_user.id
	lists=KorzinkaModel.objects.filter(haridor=user_id)
	for i in lists:
		i.address=f"{a.latitude}*{a.longitude}"
		i.save()
	s=''
	jami=0		
	for i in lists:
		if not i.is_deliver:
				s+=f"<b>{i.product}</b>\nsoni {i.soni} ta\nnarxi: {i.total/i.soni}\numumiy narxi: {i.total}\n"
				jami+=i.total
	update.message.reply_html(f"{s}\n <b>jami summa {jami}\nMa'lumotlar to'g'rimi?</b>" ,reply_markup=ReplyKeyboardMarkup([[KeyboardButton("✅ha"),
		KeyboardButton("❌yo'q")]] , resize_keyboard=True))
	# context.bot.send_location(latitude=a.latitude,
 #        longitude=a.longitude,
 #                	chat_id='1157247305' )	

def for_message(update , context):
	message=update.message.text
	user_id=update.message.from_user.id
	if message=="✅ha":
		lists=KorzinkaModel.objects.filter(haridor=user_id)
		s=''
		jami=0

		for i in lists:
			if not i.is_deliver:
				a=i.address

				s+=f"{i.product}\nsoni {i.soni} ta\nnarxi: {i.total/i.soni}\numumiy narxi: {i.total}\n"
				jami+=i.total
				i.is_deliver=True
				i.save()
		a=a.split('*')
		
		context.bot.send_location(latitude=a[0],
         longitude=a[1],
                	chat_id='1157247305' )
		context.bot.send_message(text=f"{s}\n Jami summa:{jami}", chat_id="1157247305")
		update.message.reply_text("Tez orada buyurtmangiz yetkaziladi.\n Haridingiz uchun raxmat.\nAgar yana biror narsa olishni xoxlasangiz /start ni bosing")
	elif message=="❌yo'q":
		user_id=update.message.from_user.id
		ctg=CategoryModel.objects.all()
		s=[]
		for i in ctg:
			btn=[InlineKeyboardButton(f'{i.name}' , callback_data=f'{i.id}_{user_id}_1')]
			s.append(btn)
		s.append([InlineKeyboardButton("Savatchani ko'rish" , callback_data=f'k_{user_id}_1')])	
		ctgbtn=	InlineKeyboardMarkup(s)
		update.message.reply_html("<b>Agar biror buyum sizga yoqmagan bo'lsa savatchaga o'tib o'chirib yuborishingiz mumkin</b>",
			reply_markup=ctgbtn)
