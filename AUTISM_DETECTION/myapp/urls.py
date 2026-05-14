
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('adminhome/',views.adminhome),
    path('addexpert/',views.addexpert),
    path('viewexpert/',views.viewexpert),
    path('deleteexpert/<id>',views.deleteexpert),
    path('editexpert/<id>',views.editexpert),
    path('editexpert_post/',views.editexpert_post),
    path('changepassword/',views.changepassword),
    path('viewfeedback/',views.viewfeedback),
    path('viewstudent/',views.viewstudent),
    path('logout/',views.logout_func),

    path('experthome/',views.experthome),
    path('addtips/',views.addtips),
    path('viewtips/',views.viewtips),
    path('deletetips/<id>',views.deletetips),
    path('edittips/<id>',views.edittips),
    path('edittips_post/',views.edittips_post),
    path('addstudymaterials/',views.addstudymaterials),
    path('viewstudymaterilas/',views.viewstudymaterilas),
    path('deletestudymaterials/<id>',views.deletestudymaterials),
    path('addtest/', views.addtest),
    path('viewtest/', views.viewtest),
    path('deletetest/<id>', views.deletetest),
    path('edittest/<id>', views.edittest),
    path('edittest_post/', views.edittest_post),
    path('forgotpassword/', views.forgotpassword),
    path('forgotPassword_otp/', views.forgotPassword_otp),
    path('verifyOtp/', views.verifyOtp),
    path('verifyOtpPost/', views.verifyOtpPost),
    path('new_password/', views.new_password),
    path('changePassword/', views.changePassword),
    path('expertchangepassword/', views.expertchangepassword),


    path('addquestion/<id>', views.addquestion),
    path('addquestion_post/', views.addquestion_post),
    path('expert_view_result/', views.expert_view_result),
    path('viewquestion/<id>', views.viewquestion),
    path('deletequestion/<id>', views.deletequestion),
    path('editquestion/<id>', views.editquestion),
    path('viewreport/<id>', views.viewreport),
    path('editquestion_post/', views.editquestion_post),
    path('viewparent/', views.viewparent),
    path('addguidline/<id>', views.addguidline),
    path('addguidline_post/', views.addguidline_post),
    path('viewguidline/<id>', views.viewguidline),
    path('deleteguidline/<id>', views.deleteguidline),

    path('chat/<id>', views.chat),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),

    path('chat2/<id>', views.chat2),
    path('chat_view2/', views.chat_view2),
    path('chat_send2/<msg>', views.chat_send2),

    path('register_get/',views.register_get),
    path('register/',views.register),
    path('parenthome/',views.parenthome),
    # path('parent_login/',views.parent_login),
    path('add_children_get/',views.add_children_get),
    path('add_children/',views.add_children),
    path('view_student/',views.view_children),
    path('edit_child/<id>',views.edit_child),
    path('edit_children/',views.edit_children),
    path('delete_student/<id>',views.delete_student),
    path('view_experts/',views.view_experts),
    path('add_medical_report_get/<id>',views.add_medical_report_get),
    path('add_medical_report/',views.add_medical_report),
    path('view_medical_report/<id>',views.view_medical_report),
    path('delete_medical_report/',views.delete_medical_report),
    path('parent_view_guidline/<id>',views.parent_view_guidline),
    path('view_test/',views.view_test),
    path('view_questions/<id>',views.view_questions),
    path('attend_exam_get/<id>',views.attend_exam_get),
    path('attend_exam/',views.attend_exam),
    path('view_study_material/',views.view_study_material),
    path('view_tips/',views.view_tips),
    path('send_feedback_get/',views.send_feedback_get),
    path('send_feedback/',views.send_feedback),
    path('view_result/',views.view_results),
    path('User_sendchat/',views.User_sendchat),
    path('User_viewchat/',views.User_viewchat),
    path('parent_changepassword/',views.parent_changepassword),
    path('user_check/',views.user_check),
    path('audioupload/',views.audioupload),
    path('check_autism/', views.check_autism, name='check_autism'),
    ##############
    path('check_image/',views.check_image),
    path('check_audio/',views.check_audio),
    path('process_video/',views.process_video),



    ########



    path("autism_question/", views.predict_autism_question, name="predict_question"),
    path("autism_video/", views.predict_autism_video, name="predict_video"),
    path("autism_result/", views.final_autism_result, name="final_result"),
    path("final_autism_result2/", views.final_autism_result2, name="final_autism_result2"),



]
