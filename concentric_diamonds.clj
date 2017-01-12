(def spaces (repeatedly (constantly " ")))
(def hashes (repeatedly (constantly "#")))


(defn row [total-height level]
  (let [buffer (take level spaces)
        middle-width (- total-height (* 2 level))
        middle (take middle-width (interleave hashes spaces))]
    (apply str (concat buffer middle buffer))))


(defn print-diamonds [n-diamonds]
  (let [half-height  (* 2 n-diamonds)
        total-height (+ (* 2 half-height) 1)
        printer (fn printer [level]
                  (let [row-string (row total-height level)]
                    (println row-string)
                    (when (> level 0)
                      (printer (dec level))
                      (println row-string))))]
    ;; half-height is half the height of the outermost diamond.
    ;; There is a space between each concentric diamond. Hence half-height is
    ;; 2 * n-diamonds instead of just n-diamonds.
    ;; total-height is also the total width (height and width of a diamond are equal).
    (printer half-height)))


(println)
(println "Zero diamonds:")
(println)
(print-diamonds 0)
; #

(println)
(println "One diamond:")
(println)
(print-diamonds 1)
;   #
;  # #
; # # #
;  # #
;   #

(println)
(println "Two diamonds:")
(println)
(print-diamonds 2)
;     #
;    # #
;   # # #
;  # # # #
; # # # # #
;  # # # #
;   # # #
;    # #
;     #

(println)
(println "Three diamonds:")
(println)
(print-diamonds 3)
;       #
;      # #
;     # # #
;    # # # #
;   # # # # #
;  # # # # # #
; # # # # # # #
;  # # # # # #
;   # # # # #
;    # # # #
;     # # #
;      # #
;       #

(println)
(println "Four diamonds:")
(println)
(print-diamonds 4)
;         #
;        # #
;       # # #
;      # # # #
;     # # # # #
;    # # # # # #
;   # # # # # # #
;  # # # # # # # #
; # # # # # # # # #
;  # # # # # # # #
;   # # # # # # #
;    # # # # # #
;     # # # # #
;      # # # #
;       # # #
;        # #
;         #


; (println)
; (print-diamonds 25)

(println)
