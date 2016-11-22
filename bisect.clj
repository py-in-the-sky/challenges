(defn bisect-left [v x]
  (loop [lo 0 hi (count v)]
    ;; Loop invariants:
    ;;   - everything to the left of lo is < x
    ;;   - everything at or to the right of hi is >= x
    ;; In the end, lo == hi and lo is the leftmost spot that is >= x.
    (let [mid (int (/ (+ lo hi) 2))]
      (cond
        (= lo hi) lo
        (< (get v mid) x) (recur (inc mid) hi)
        :else (recur lo mid)))))

(defn bisect-right [v x]
 (loop [lo 0 hi (count v)]
   ;; Loop invariants:
   ;;   - everything to the left of lo is <= x
   ;;   - everything at or to the right of hi is > x
   ;; In the end, lo == hi and lo is the leftmost spot that is > x.
   (let [mid (int (/ (+ lo hi) 2))]
      (cond
        (= lo hi) lo
        (> (get v mid) x) (recur lo mid)
        :else (recur (inc mid) hi)))))
