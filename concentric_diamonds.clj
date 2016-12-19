(def spaces (repeatedly (constantly " ")))
(def hashes (repeatedly (constantly "#")))


(defn row [total-height level]
  (let [buffer-width level
        middle-width (- total-height (* 2 buffer-width))
        left-buffer  (take buffer-width spaces)
        middle       (take middle-width (interleave hashes spaces))
        right-buffer left-buffer]
    (apply str (concat left-buffer middle right-buffer))))


(defn print-diamonds-helper [level row-fn]
  (let [row-string (row-fn level)]
    (println row-string)
    (when (> level 0)
      (print-diamonds-helper (dec level) row-fn)
      (println row-string))))


(defn print-diamonds [n-diamonds]
  (let [half-height  (* 2 n-diamonds)
        total-height (+ (* 2 half-height) 1)]
    ;; half-height is half the height of the outermost diamond.
    ;; There is a space between each concentric diamond. Hence half-height is
    ;; 2 * n-diamonds instead of just n-diamonds.
    ;; total-height is also the total width (height and width of a diamond are equal).
    (print-diamonds-helper half-height #(row total-height %))))


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
