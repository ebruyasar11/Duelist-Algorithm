import numpy as np
import random
import time
import matplotlib.pyplot as mp

class Duellocu_Algoritmasi():
	def __init__(self,f,x,altdeger,ustdeger,pop=200,sans=0.01,mutasyon=0.1,ogren=0.8,iterasyon=500,nc=5,karistir=False):
		#Sınıf değişkenlerinin tanımlamaları
		self.f = f
		self.x = x
		self.altdeger = altdeger
		self.ustdeger = ustdeger
		self.populasyon = pop
		self.sans = sans
		self.mutasyon = mutasyon
		self.ogren = ogren
		self.max_iterasyon = iterasyon
		self.nc = nc
		self.sampiyon = np.empty((x.__len__()+1,nc),dtype=np.float64)
		self.kazan_kaybet = np.empty((pop,1),dtype=np.float64)
		self.savas_puani = np.empty((pop,1),dtype=np.float64)
		self.iterasyon = 0
		self.karistir = karistir
		self.x_dizi = []
		self.y_dizi = []
		self.fmin = []
		#Çok değişkenli optimizasyonun yapılıp yapılmayacağının kontrolünü yapar 
		if type(x) is list:
			self.mult=1
			assert x.__len__()==altdeger.__len__()==ustdeger.__len__() , "Sinir hatasi, lutfen altdeger ve ustdegeri kontrol edin"
		else:
			self.mult=0
		
		#Hesaplama için başlangıç matrisi oluşturur
		if self.mult==1:
			shape=(x.__len__(),pop)
		else:
			shape=(1,pop)
		self.matrix=np.empty(shape,dtype=np.float64)
		self.egitim=np.empty(shape,dtype=np.float64)
		self.puan=np.empty(pop,dtype=np.float64)
		self.cozum_degeri=np.empty((x.__len__()+1,pop),dtype=np.float64)
		self.en_iyi_cozum=np.empty((0,x.__len__()+1),dtype=np.float64)
		
	def baslangic(self,plot=False):
		self.plot=plot
		#Düellocu algoritma adımları
		self.kayit()
		self.yeterlilik()
		while self.iterasyon < self.max_iterasyon:
			self.sampiyon_sec()
			self.duello()
			self.duellocu_egitimi()
			self.yeterlilik_sonrasi()
			self.ele()
			self.iterasyon=self.iterasyon+1
		self.sonuc_goster()

	def kayit(self):
		#Düello kayıt
		for i in range(0,self.x.__len__()):
		#Popülasyonu başlatmak için sözde rastgele oluşturucu
			t = int( time.time() * 1000.0 )
			np.random.seed( ((t & 0xff000000) >> 24) +
             ((t & 0x00ff0000) >>  8) +
             ((t & 0x0000ff00) <<  8) +
             ((t & 0x000000ff) << 24)   )
			#Oluşturulan matrisi alt ve ust degere göre sınırla
			self.matrix[i,:]=np.random.uniform(size=self.populasyon,low=self.altdeger[i],high=self.ustdeger[i])


	def yeterlilik(self):
		#Bu bölüm yalnızca nüfus iki katına çıktığında yeterlilik sonrası için işe yarar
		if self.puan.shape[0]<self.matrix.shape[1]:
			self.puan=np.append(self.puan,self.puan)
		#Uygunluk fonksiyonuna göre bir uygunluk degeri hesapla
		for i in range(0,self.matrix.shape[1]):
			self.puan[i]=self.f(*self.matrix.T.tolist()[i])
		self.puani_degerlendir()

	def puani_degerlendir(self):
		#Çözümleri en düşükten en yükseğe doğru sırala
		self.puan=np.asarray([self.puan])
		self.cozum_degeri=np.concatenate((self.puan,self.matrix),axis=0).T
		
		self.cozum_degeri=self.cozum_degeri[self.cozum_degeri[:,0].argsort()].T
		self.puan=self.cozum_degeri[0,:]
		self.matrix=self.cozum_degeri[1:,:]
	
	def yeterlilik_sonrasi(self):
		#Matrisi sıralayabilmek için transpozunu al
		self.matrix=self.matrix.T
		#Tekrar karşılaştır
		self.yeterlilik()
		
	def sampiyon_sec(self):
		#En iyi şampiyonu kaydet
		for i in range(0,self.nc):
			self.en_iyi_cozum=np.concatenate((self.en_iyi_cozum,np.asarray([self.cozum_degeri[:,i]])))
		#Şampiyonları tüm sonuçlardan ayır
		self.sampiyon=self.cozum_degeri[:,0:self.nc]
		print(f"{self.iterasyon + 1}. iterasyon, cozum degeri {self.cozum_degeri[:,0][0]}, fmin {self.cozum_degeri[:,0][1::]}")
		self.cozum = []	
		self.cozum.append(self.cozum_degeri[:,0][1::])
		self.x_dizi.append(self.cozum[0][0])
		self.y_dizi.append(self.cozum[0][1])

		if self.fmin.__len__()==0:
			self.fmin.append(self.cozum_degeri[:,0][0])
		elif self.cozum_degeri[:,0][0]<min(self.fmin):
			self.fmin.append(self.cozum_degeri[:,0][0])
		else:
			self.fmin.append(min(self.fmin))
		#Benzer şampiyonları tekrar eğit
		for j in range(0,self.nc):
			for i in range(0,self.x.__len__()):
				if (random.uniform(0,1)<self.mutasyon):
					self.matrix[i,j]=random.uniform(self.altdeger[i],self.ustdeger[i])
		
	def duello(self):
		#Düellocuları popülasyondan rastgele eşleştir
		self.matrix=self.matrix.T
		if(self.karistir==True):
			np.random.mut(self.matrix)
		
		#Düello kuralları
		i=0
		while i<self.matrix.shape[0]:
			#nüfus tekse, eşleşmeyen düellocu otomatik olarak kazanır
			if(i==self.matrix.shape[0]-1):
				self.kazan_kaybet[i]=1
			else:
			#iki düellocu için savaş puanını hesapla
				tempmatrix=self.matrix.tolist()
				self.savas_puani[i]=self.f(*tempmatrix[i])*(1+(self.sans+(random.uniform(0,1)*self.sans)))
				self.savas_puani[i+1]=self.f(*tempmatrix[i+1])*(1+(self.sans+(random.uniform(0,1)*self.sans)))
			#savaş puanına göre kazananı ve kaybedeni belirle
				if(self.savas_puani[i]>self.savas_puani[i+1]):
					self.kazan_kaybet[i]=1
					self.kazan_kaybet[i+1]=0
				else:
					self.kazan_kaybet[i]=0
					self.kazan_kaybet[i+1]=1
			i=i+2
	
	def duellocu_egitimi(self):
		#Kazanan ve kaybedene göre eğit
		self.egitim=np.copy(self.matrix)
		for j in range(0,self.x.__len__()):
			for i in range(0,self.populasyon):
				if self.kazan_kaybet[i]==1:
				#kazanan mutasyona uğrayarak kendini geliştirsin
					if random.uniform(0,1)<self.mutasyon:
						self.egitim[i,j]=random.uniform(self.altdeger[j],self.ustdeger[j])
				else:
				#Kaybeden kazanandan öğrensin
					if random.uniform(0,1)<self.ogren:
						if (i%2==0):
							self.egitim[i,j]=self.matrix[i+1,j]
						else:
							self.egitim[i,j]=self.matrix[i-1,j]
		#Matrise yeni eğitilmiş düellocu ekle
		self.matrix=np.concatenate((self.matrix,self.egitim),axis=0)
	
	def ele(self):
		self.matrix=self.matrix[:,:self.populasyon]
		
	def sonuc_goster(self):
		sonuc=self.en_iyi_cozum[self.en_iyi_cozum[:,0].argsort()]
		print("En iyi cozum degerleri:",sonuc[0][1::], "En iyi cozum", sonuc[0][0])
		if self.plot==True:
			fig = fig = mp.figure()
			ax1 = fig.add_subplot(211)
			ax1.plot(self.fmin,'r.-')
			ax1.legend(['MinUygunluk'])
			ax2 = fig.add_subplot(212)
			ax2.plot(self.x_dizi,'b.-')
			ax2.plot(self.y_dizi,'g--')
			mp.legend(['x1','x2'])
			mp.show()
		
	