#-----------------------------------------------------
# ここで杉村流の，このPythonファイルのカレントディレクトリの取得方法

import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
#-----------------------------------------------------
import time
import cv2
import mediapipe as mp
import datetime

# test module#######################
from testcsv import outputcsv
#######################

# from image import IMAGE_FILES
from get_images import get_images
from hands_output_csv import  recognized_image_change_name, get_id_label, get_Handedness, get_landmark , get_label_en, get_label_ja,get_current_dir
from function_get_current import get_current_yyyy_mm_dd
from data_recognize_hand import DataRecognizeHand
from output_csv_file import output_csv
from tqdm.auto import tqdm
# from output_csv.file import output_csv
# from input_csv_file import inputDate
# from ja_dict import ja_dict
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For static images:

with mp_hands.Hands(
		static_image_mode=True,
		max_num_hands=2,
		min_detection_confidence=0.5) as hands:

	# for i in range(len(files_name)):from
	# 	  print("files name:", files_name[i])

	# key = 0 ... it can get the data don't recognize 
	# key = 1 ... it can get the data recognized
	# key = all ... it can get all of the data

	key = "ALL"
	IMAGE_FILES = get_images(PYPATH, key)
	for i in tqdm(range(len(IMAGE_FILES)),desc="loading"):

		# Read an image, flip it around y-axis for correct handedness output (see
		# above).
		image = cv2.flip(cv2.imread(IMAGE_FILES[i]), 1)
		# Convert the BGR image to RGB before processing.
		results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

		# Print handedness and draw hand landmarks on the image.
		# ハンドネスのプリント
		# print('Handedness:', results.multi_handedness)
		if not results.multi_hand_landmarks:
			continue
		image_height, image_width, _ = image.shape
		annotated_image = image.copy()


		for hand_landmarks in results.multi_hand_landmarks:
    			
			
			for_id_from_score_List = []
			#　以下実行->ランドマークの数値がプリントされる
			# print('filename:',file)

			refile = recognized_image_change_name(IMAGE_FILES[i])
			
			
			create_date = get_current_yyyy_mm_dd()
			id_label = get_id_label(refile)
			label_en = get_label_en(refile)
			filedir = get_current_dir(refile)
			label_ja = get_label_ja(label_en)
			left_or_right_score, left_or_right_label = get_Handedness(results.multi_handedness)
			landmarks_List = get_landmark(results.multi_hand_landmarks)
			
			for_id_from_score_List.append(create_date)
			for_id_from_score_List.append(id_label)
			for_id_from_score_List.append(label_en)
			for_id_from_score_List.append(label_ja)
			for_id_from_score_List.append(filedir)
			for_id_from_score_List.append(left_or_right_label)
			for_id_from_score_List.append(left_or_right_score)
			# for_id_from_score_List.append(landmarks_List)


			# print(for_id_from_score_List)
			# print(landmarks_List)

			dataRecognizeHand_obj = DataRecognizeHand(
				create_date,
				id_label,
				label_en,
				label_ja,
				filedir,
				left_or_right_label,
				left_or_right_score,
				landmarks_List
				)

			output_csv(dataRecognizeHand_obj)
			
			

			# outputcsv(id, create_date, id_in_label, label_ja, label_en, file_dir, left_or_right_label, left_or_right_score, landmarks_List)
			# print('Handedness:', results.multi_handedness)
			# print('hand_landmarks:', hand_landmarks)
			# print(
			#     f'Index finger tip coordinates: (',
			#     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
			#     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
			# )
			# ここでランドマーク(骨格ぽいんた？)の，画像への描写してる
			#mp_drawing.draw_landmarks(
			#  annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

		# ここで画像の保存してる？
		# /tmpってWindowsでどこやねんｗ
		# cv2.imwrite(
		#     '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

		# hiragana = input("平仮名を入力してください:")
		# romaji = ja_dict[hiragana]

		# hand_label = results.multi_handedness

		# fingerTip_x = "{x}".format(x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
		# fingerTip_y = "{y}".format(y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)

		#数値データをCSVへ書き出し
		# inputDate(hiragana, romaji, hand_label, results.multi_hand_landmarks)

		# 画像の保存ではなく表示の方でためそう
		## => OKそう
		# while True:
		#   cv2.imshow('MediaPipe Hands', annotated_image)
		#   if cv2.waitKey(5) & 0xFF == 27:
		#     # ここをやると一枚ずつ切り替わる
		#     break
		#   time.sleep(1)




# # For webcam input:
# cap = cv2.VideoCapture(1)   #REN...camera number 1 Yuri...0
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FOURCC, 0x32595559)
# cap.set(cv2.CAP_PROP_FPS, 60)
# with mp_hands.Hands(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as hands:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # Flip the image horizontally for a later selfie-view display, and convert
#     # the BGR image to RGB.
#     image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     results = hands.process(image)

#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#       for hand_landmarks in results.multi_hand_landmarks:
#         mp_drawing.draw_landmarks(
#             image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#     cv2.imshow('MediaPipe Hands', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()