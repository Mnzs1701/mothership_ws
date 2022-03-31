
(cl:in-package :asdf)

(defsystem "multi_robot-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "gotoAction" :depends-on ("_package_gotoAction"))
    (:file "_package_gotoAction" :depends-on ("_package"))
    (:file "gotoActionFeedback" :depends-on ("_package_gotoActionFeedback"))
    (:file "_package_gotoActionFeedback" :depends-on ("_package"))
    (:file "gotoActionGoal" :depends-on ("_package_gotoActionGoal"))
    (:file "_package_gotoActionGoal" :depends-on ("_package"))
    (:file "gotoActionResult" :depends-on ("_package_gotoActionResult"))
    (:file "_package_gotoActionResult" :depends-on ("_package"))
    (:file "gotoFeedback" :depends-on ("_package_gotoFeedback"))
    (:file "_package_gotoFeedback" :depends-on ("_package"))
    (:file "gotoGoal" :depends-on ("_package_gotoGoal"))
    (:file "_package_gotoGoal" :depends-on ("_package"))
    (:file "gotoResult" :depends-on ("_package_gotoResult"))
    (:file "_package_gotoResult" :depends-on ("_package"))
  ))